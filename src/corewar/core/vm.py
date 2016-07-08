# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data             import const
from corewar.core.data.circuit     import Circuit
from corewar.core.data.ship        import Ship
from corewar.core.pit.pit          import Pit
from corewar.core.instrset.decoder import Decoder
from pyscript.logger.object        import LoggingObject
from pyscript.exceptions           import BaseException

# ---------------------------------------------------------------------------- #

class VirtualMachine(LoggingObject):
    class States:
        Uninitialized = 1
        Ready         = 2
        Running       = 3
        Finished      = 4
    class League:
        Race     = 1
        Fight    = 2

    def __init__(self, p_leagueMode, p_logHandlers=None):
        LoggingObject.__init__(self,  "vm", p_logHandlers)
        self.registerHandler("init",    "[init]")
        self.registerHandler("js_init", "[init]")
        self.registerHandler("cycle",   "[cycle]")
        self.registerHandler("read",    "[read]")
        self.registerHandler("fetch",   "[fetch]")
        self.registerHandler("delay",   "[delay]")
        self.registerHandler("execute", "[execute]")
        self.registerHandler("write",   "[write]")
        self.registerHandler("other",   "[other]")

        self.m_circuit     = Circuit()
        self.m_ships       = []
        self.m_pit         = Pit()
        self.m_state       = VirtualMachine.States.Uninitialized
        self.m_league      = p_leagueMode
        self.m_decoder     = Decoder()
        self.m_cycleID     = 0
        self.m_dataInit    = []
        self.m_dataCycle   = []
        self.m_dataFinish  = []

    def addShipCode(self, p_shipCode):
        l_nextShipID = len(self.m_ships)
        self.info("init", "adding ship #%d", l_nextShipID)
        l_ship = self.m_pit.buildShipCode(p_shipCode, l_nextShipID)
        self.addShip(l_ship)

    def addShipSource(self, p_shipSource):
        l_nextShipID = len(self.m_ships)
        self.info("init", "adding ship #%d : %s", l_nextShipID, p_shipSource)
        l_ship = self.m_pit.buildShipSource(p_shipSource, l_nextShipID)
        self.addShip(l_ship)

    def addShip(self, p_ship):
        if p_ship == None:
            self.error("init", "unable to parse ship file")
            return

        if p_ship.getOwner() in [ x.getOwner() for x in self.m_ships ]:
            self.warning("init", "ship name '%s' already registered", p_ship.getOwner())
            self.m_dataInit.append({
                "id"        : p_ship.getID(),
                "start_pos" : 0,
                "status"    : "disqualified",
                "name"      : p_ship.m_owner,
                "code"      : []
            })
            p_ship.setDisqualified()
        self.m_ships.append(p_ship)

    def initialize(self):
        self.info("init", "initializing machine")

        if self.m_state != VirtualMachine.States.Uninitialized:
            self.error("init", "already initialized")
            return False

        l_ships = filter(Ship.isRunningStatus, self.m_ships)
        if 0 == len(l_ships):
            self.error("init", "need at leat one ship to run")
            return False

        self.m_circuit.generateChunks(const.MEMORY_SIZE)
        l_shipMaxSize = const.MEMORY_SIZE / len(l_ships)
        for c_ship in l_ships:
            if c_ship.getSize() > l_shipMaxSize:
                c_ship.setDisqualified()
                self.warning("init", "ship #%d disqualified, code size '%d' is too big", c_ship.getID(), c_ship.getSize())
                self.m_dataInit.append({
                    "id"        : l_shipPos,
                    "name"      : c_ship.m_owner,
                    "start_pos" : 0,
                    "status"    : "disqualified",
                    "code"      : []
                })

        l_ships = filter(Ship.isRunningStatus, self.m_ships)
        l_shipPos = 0
        for c_ship in l_ships:
            l_startChunkID = l_shipPos * l_shipMaxSize
            self.info("init", "ship #%d start pos is %d", l_shipPos, l_startChunkID)
            self.m_dataInit.append({
                "id"        : l_shipPos,
                "name"      : c_ship.m_owner,
                "start_pos" : l_startChunkID,
                "status"    : "running",
                "code" : [ x.getValue() for x in c_ship.getInitialCode() ]
            })
            self.m_circuit.placeShip(c_ship, l_startChunkID)
            self.info("init", "dumping ship initial code")
            for c_chunkID in range(len(c_ship.getInitialCode())):
                self.info("init", "%s", self.m_circuit.getChunkByID(c_chunkID + l_startChunkID))
            c_ship.setPC(l_startChunkID)
            c_ship.setInitialPC(l_startChunkID)
            l_shipPos += 1

        self.m_state = VirtualMachine.States.Ready
        return True


    def run(self):
        self.info("cycle", "cycle #%d : starting race", self.m_cycleID)
        if self.m_state != VirtualMachine.States.Ready:
            self.error("cycle", "vm not initialized")
            return None

        self.m_state = VirtualMachine.States.Running
        while self.m_state == VirtualMachine.States.Running:
            self.m_cyleInfo = { "cycle" : self.m_cycleID }
            self.info("cycle", "cycle #%d : begin cycle", self.m_cycleID)
            l_ships = filter(Ship.isRunningStatus, self.m_ships)
            self.m_cyleInfo["ships"] = {}
            for c_ship in l_ships:
                self.m_cyleInfo["ships"][c_ship.getID()] = {}
                self.m_cyleInfo["ships"][c_ship.getID()]["actions"] = []

            self.resolveWinners(l_ships)
            self.resolveDeads(l_ships)
            l_ships = filter(Ship.isRunningStatus, l_ships)
            self.resolveShips(l_ships)
            self.resolveWrites(l_ships)
            self.resolveForks(l_ships)
            self.resolveChecks(l_ships)
            self.m_cycleID += 1
            self.m_dataCycle.append(self.m_cyleInfo)
            map(lambda x:x.setNbCycle(self.m_cycleID), l_ships)
        self.info("cycle", "cycle #%d : finishing race", self.m_cycleID)
        return self.m_ships

    def resolveWinners(self, p_ships):
        """
        1. race stops with no winner if there is no running ships
        2. race stops with some winners if any ships ran LAPS * MEMSIZE
        3. race stops with winner if all running ships belongs to same owner
        """
        # 1.
        if len(p_ships) == 0:
            self.info("other", "cycle #%d : no more running ships, stopping race", self.m_cycleID)
            self.m_state = VirtualMachine.States.Finished

        # 2.
        if self.m_league == VirtualMachine.League.Race:
            for c_ship in p_ships:
                if c_ship.getLastCheckWO() >= const.LAPS_NUMBER * const.MEMORY_SIZE:
                    c_ship.setWinner()
                    self.info("other", "cycle #%d / ship #%d : detected as winner", self.m_cycleID, c_ship.getID())
                    self.m_dataFinish.append({ "id" : c_ship.getID(), "status" : "winner" })
                    self.m_state = VirtualMachine.States.Finished

        # 3.
        elif self.m_league == VirtualMachine.League.Fight:
            l_owners = set(tuple(c_ship.getOwner()) for c_ship in p_ships);
            if len(l_owners) == 1:
                self.info("other", "cycle #%d : '%s' detected as winner", self.m_cycleID, p_ships[0].getOwner())
                self.m_state = VirtualMachine.States.Finished
                map(Ship.setWinner, p_ships)

    def resolveDeads(self, p_ships):
        """
        1. no need to use Ship.m_lastCheckID, that is only usefull for resolveChecks

        notes :
          remove loosers to place new forks ?
          no, just count running ships on ship fork limit !
        """
        # 1.
        for c_ship in p_ships:
            if self.m_cycleID >= c_ship.getLastCheckCycle() + const.CHECKPOINT_DELAY:
                self.info("other", "cycle #%d / ship #%d : last check cycle (%d) is too old, setting killing",
                          self.m_cycleID,
                          c_ship.getID(),
                          c_ship.getLastCheckCycle())
                self.m_cyleInfo["ships"][c_ship.getID()]["actions"].append({"action" : "dead"})
                c_ship.setDead()

    def resolveShips(self, p_ships):
        """
        1. resolution cycles until some action actually consume a cycle
           some actions may be free when using blue arrow or rail
        2. ship needs to read circuit to build an instruction
           we check if read chunk created a valid instruction and if so,
           ship switch to decode state
        3. ship slowly decrements delay, cycle is consumed only if decode
           is not null. if delay is null, ship switch to execute state
        4. same goes for executing. note that some instructions hasmultiple
           execution stages
        """

        for c_ship in p_ships:
            l_info = self.m_cyleInfo["ships"][c_ship.getID()]["actions"]
            self.info("cycle", "cycle #%d / ship #%d : processing ship (pc = %d, wo = %d)",
                      self.m_cycleID,
                      c_ship.getID(),
                      c_ship.getPC(),
                      c_ship.getWO())
            l_freeCycle = True
            # 1.
            while l_freeCycle:
                # 2.
                if c_ship.isReadingState():
                    l_chunk = self.m_circuit.getChunkFromShip(c_ship)
                    self.info("read", "cycle #%d / ship #%d : reading : %s", self.m_cycleID, c_ship.getID(), str(l_chunk))
                    self.m_circuit.moveShip(c_ship, 1)
                    c_ship.addQueue(l_chunk)
                    l_info.append({
                        "action"  : "read",
                        "offset"  : c_ship.getPC(),
                        "value"   : l_chunk.getValue(),
                        "queue"   : [ x.getValue() for x in c_ship.getQueue() ]
                    })

                    l_instr = self.m_decoder.decode(c_ship, self.m_circuit, self.m_cycleID)
                    if l_instr != None:
                        self.info("fetch", "cycle #%d / ship #%d : fecthed : %s", self.m_cycleID, c_ship.getID(), str(l_instr))
                        l_info.append({
                            "action"  : "fetch",
                            "instr"   : str(l_instr),
                            "decode"  : l_instr.getDecodeDelay(),
                            "execute" : l_instr.getExecuteDelay(),
                        })
                        l_info.append({
                            "action" : "state",
                            "state"  : "decoding"
                        })
                        c_ship.setInstr(l_instr)
                        c_ship.setDecodeDelay(c_ship.getCurrentInstr().getDecodeDelay())
                        c_ship.setDecodingState()
                    l_freeCycle = False

                # 3.
                elif c_ship.isDecodingState():
                    l_cycleLeft = c_ship.getDecodeDelay()
                    self.info("delay", "cycle #%d / ship #%d : decoding wait : %d", self.m_cycleID, c_ship.getID(), l_cycleLeft)
                    if l_cycleLeft != 0:
                        c_ship.setDecodeDelay(l_cycleLeft - 1)
                        l_freeCycle = False
                    l_cycleLeft = c_ship.getDecodeDelay()
                    if l_cycleLeft == 0:
                        self.info("delay", "cycle #%d / ship #%d : decode", self.m_cycleID, c_ship.getID())
                        l_info.append({
                            "action"  : "state",
                            "state"   : "executing"
                        })
                        c_ship.setExecuteDelay(c_ship.getCurrentInstr().getExecuteDelay())
                        c_ship.setExecutingState()
                    else:
                        l_info.append({
                            "action"  : "decoding",
                            "left"    : l_cycleLeft
                        })
                # 4.
                elif c_ship.isExecutingState():
                    l_cycleLeft = c_ship.getExecuteDelay()
                    self.info("delay", "cycle #%d / ship #%d : executing wait : %d", self.m_cycleID, c_ship.getID(), l_cycleLeft)
                    if c_ship.getExecuteDelay() != 0:
                        c_ship.setExecuteDelay(l_cycleLeft - 1)
                        l_freeCycle = False

                    l_cycleLeft = c_ship.getExecuteDelay()
                    if l_cycleLeft == 0:
                        self.info("execute", "cycle #%d / ship #%d : execute : %s", self.m_cycleID, c_ship.getID(), str(c_ship.getCurrentInstr()))
                        c_ship.getCurrentInstr().doExecute(l_info)
                        if c_ship.getCurrentInstr().isFinished():
                            l_info.append({
                                "action"  : "state",
                                "state"   : "reading"
                            })
                            c_ship.setReadingState()
                        else:
                            c_ship.setExecuteDelay(c_ship.getCurrentInstr().getExecuteDelay())
                            l_info.append({
                                "action"  : "executing",
                                "left"    : c_ship.getCurrentInstr().getExecuteDelay()
                            })
                    else:
                        l_info.append({
                            "action"  : "executing",
                            "left"    : l_cycleLeft
                        })

            self.m_cyleInfo["ships"][c_ship.getID()]["pc"] = c_ship.getPC()
            self.m_cyleInfo["ships"][c_ship.getID()]["wo"] = c_ship.getWO()

    def resolveWrites(self, p_ships):
        # warning: hack to avoid full scan of the circuit looking
        # for votes. Votes should be stocked in the VM in some smart way.
        # chunk might not need to have votes as member, after all.
        self.m_cyleInfo["writes"] = []
        l_writes = self.m_cyleInfo["writes"]
        for c_chunkID in self.m_circuit.m_writes:
            l_chunk = self.m_circuit.m_chunks[c_chunkID]
            self.info("write", "cycle #%d : chunk : %s", self.m_cycleID, str(l_chunk))
            for c_bit in range(4):
                l_sum = sum(1 if c_vote.getBit(c_bit) else -1 for c_vote in l_chunk.getVotes())
                if l_sum > 0:
                    l_chunk.getData().setBit(c_bit, True)
                elif l_sum < 0:
                    l_chunk.getData().setBit(c_bit, False)
            l_writes.append({
                "chunkid" : c_chunkID,
                "value"   : l_chunk.getValue()
            });
            l_chunk.clearVotes()
            l_chunk.setWroteLastCycle(self.m_cycleID)
        self.m_circuit.m_writes = []


    def resolveForks(self, p_ships):
        l_totalShipCount = len(self.m_ships)
        l_newShips = []
        for c_ship in p_ships:
            if c_ship.getForkState():
                self.info("other", "cycle #%d / ship #%d : forking ship", self.m_cycleID, c_ship.getID())
                if l_totalShipCount < const.MAX_NB_SHIPS:
                    self.info("other", "cycle #%d / ship #%d : fork accepted, new id #%d", self.m_cycleID, c_ship.getID(), l_totalShipCount)
                    l_ship = c_ship.fork(l_totalShipCount)
                    l_newShips.append(l_ship)
                    l_totalShipCount += 1
                c_ship.setZ(False)
                c_ship.setForkState(False)
        self.m_ships += l_newShips

    def resolveChecks(self, p_ships):
        for c_ship in p_ships:
            l_info = self.m_cyleInfo["ships"][c_ship.getID()]["actions"]
            if c_ship.getCheckState():
                l_minWO = c_ship.getLastCheckWO() + 1 * const.CHECKPOINT_SIZE
                l_maxWO = c_ship.getLastCheckWO() + 2 * const.CHECKPOINT_SIZE
                self.info("other", "cycle #%d / ship #%d : verifiyng check (wo = %d, min wo = %d, max wo = %d)", self.m_cycleID, c_ship.getID(), c_ship.getLastCheckWO(), l_minWO, l_maxWO)
                if (c_ship.getWO() >= l_minWO) and (c_ship.getWO() <  l_maxWO):
                    c_ship.setLastCheckWO(c_ship.getLastCheckWO() + const.CHECKPOINT_SIZE)
                    c_ship.setLastCheckCycle(self.m_cycleID)
                    self.info("other", "cycle #%d / ship #%d : check validated", self.m_cycleID, c_ship.getID())
                    l_info.append({
                        "action"         : "check",
                        "next_min_check" : l_maxWO,
                        "next_max_check" : l_maxWO + const.CHECKPOINT_SIZE,
                    })
            c_ship.setCheckState(False)



    def filterResults(self, p_ships, p_type = "best"):

        def cmpShip(p_ship1, p_ship2):
            if ((p_ship1.getStatus() == Ship.Status.Winner) and
                (p_ship2.getStatus() == Ship.Status.Winner)):
                return cmp(p_ship1.getNbCycle(), p_ship2.NbCycle())
            elif ((p_ship1.getStatus() != Ship.Status.Winner) and
                  (p_ship2.getStatus() == Ship.Status.Winner)):
                return -1
            elif ((p_ship1.getStatus() == Ship.Status.Winner) and
                  (p_ship2.getStatus() != Ship.Status.Winner)):
                return 1
            elif ((p_ship1.getStatus() != Ship.Status.Winner) and
                  (p_ship2.getStatus() != Ship.Status.Winner)):
                return cmp(p_ship1.getWO(), p_ship2.getWO())

        l_param  = p_type
        l_result = []
        if l_param == "all":
            l_result = p_ships
        elif l_param == "best":
            p_ships.sort(cmp=cmpShip, reverse=True)
            for c_ship in p_ships:
                if 0 == cmpShip(c_ship, p_ships[0]):
                    l_result.append(c_ship)
        elif l_param == "bestofuser":
            l_users = []
            for c_ship in p_ships:
                if c_ship.getOwner() not in l_users:
                    l_users.append(c_ship.getOwner())
            for c_user in l_users:
                l_ships = filter(lambda x:x.getOwner() == c_user, p_ships)
                l_ships.sort(cmp=cmpShip, reverse=True)
                for c_ship in l_ships:
                    if 0 == cmpShip(c_ship, l_ships[0]):
                        l_result.append(c_ship)
            l_result.sort(cmp=cmpShip, reverse=True)
        return l_result

    def printResult(self, p_ships):
        l_ships = self.filterResults(p_ships)
        l_str = "+--------------------------------------------------------------+\n"
        for c_ship in l_ships:
            l_str += "|    name : %-50s |\n" % c_ship.getOwner()
            l_str += "|  status : %-50s |\n" % c_ship.getStatus()
            l_str += "| comment : %-50s |\n" % c_ship.getComment()
            l_str += "| ship id : #%-49s |\n" % c_ship.getID()
            l_str += "|  cycles : %-50s |\n" % c_ship.getNbCycle()
            l_str += "|    mode : %-50s |\n" % c_ship.getMode().Name
            l_str += "|      pc : %-50s |\n" % c_ship.getPC()
            l_str += "|      wo : %-50s |\n" % c_ship.getWO()
            l_str += "+--------------------------------------------------------------+\n"
        return l_str
