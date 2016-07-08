# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

import copy
from corewar.core.data         import const
from corewar.core.data.quartet import Quartet, Register
from corewar.core.data.chunk   import Chunk
from corewar.core.data.modes   import Modes

# ---------------------------------------------------------------------------- #


class Ship:
    class Status:
        Winner       = 1
        Running      = 2
        Disqualified = 3
        Crashed      = 4
        Dead         = 5
    class States:
        Reading   = 1
        Decoding  = 2
        Executing = 3

    def __init__(self, p_id):
        self.m_id             = p_id;
        self.m_registers      = [ Register("r%d" % x) for x in range(16) ]
        self.m_buffer         = [ Quartet()  for x in range(64) ]
        self.m_wo             = 0
        self.m_z              = False;
        self.m_s              = False;
        self.m_pc             = 0;
        self.m_queue          = [] # [ Quartet() for x in range(7) ]
        self.m_mode           = Modes.Feisar
        self.m_owner          = ""
        self.m_comment        = ""
        self.m_lastCheckWO    = 0
        self.m_lastCheckCycle = 0
        self.m_initialCode    = [] # [ Quartet() for x in range(const.MAX_CODE_SIZE) ]
        self.m_status         = Ship.Status.Running
        self.m_state          = Ship.States.Reading
        self.m_forkState      = False
        self.m_checkState     = False
        self.m_initialPC      = 0
        self.m_decodeDelay    = 0
        self.m_executeDelay   = 0
        self.m_instr          = None
        self.m_nbCycle        = 0

    def __str__(self):
        return """
 id : %d
 owner : %s
 comment : %s
 status : %s
 pc : %d
 wo : %d
 s  : %d
 z  : %d
 r0 : %s
 r1 : %s
 r2 : %s
 r3 : %s
""" % (self.m_id, self.m_owner, self.m_comment, self.m_status,
       self.m_pc, self.m_wo, self.m_s, self.m_z,
       self.m_registers[0], self.m_registers[1],
       self.m_registers[2], self.m_registers[3])

    def addInitialCode(self, p_quartet):
        self.m_initialCode.append(p_quartet)

    def getSize(self):
        return len(self.m_initialCode)
    def getInitialCode(self):
        return self.m_initialCode

    def fork(self, p_newID):
        l_ship = Ship(p_newID)
        l_ship.m_registers      = copy.deepcopy(self.m_registers)
        l_ship.m_buffer         = copy.deepcopy(self.m_buffer)
        l_ship.m_wo             = self.m_wo
        l_ship.m_z              = True
        l_ship.m_s              = self.m_s
        l_ship.m_pc             = self.m_pc
        l_ship.m_queue          = copy.deepcopy(self.m_queue)
        l_ship.m_mode           = self.m_mode
        l_ship.m_owner          = self.m_owner
        l_ship.m_comment        = self.m_comment
        l_ship.m_lastCheckWO    = self.m_lastCheckWO
        l_ship.m_lastCheckCycle = self.m_lastCheckCycle
        l_ship.m_initialCode    = []
        l_ship.m_status         = self.m_status
        l_ship.m_state          = self.m_state
        l_ship.m_forkState      = False
        l_ship.m_checkState     = self.m_checkState
        l_ship.m_initialPC      = self.m_initialPC
        l_ship.m_decodeDelay    = self.m_decodeDelay
        l_ship.m_executeDelay   = self.m_executeDelay
        l_ship.m_instr          = None
        l_ship.m_nbCycle        = self.m_nbCycle
        return l_ship

    def writeBuffer(self, p_quart, p_offset = 0):
        l_offset = p_offset % len(self.m_buffer)
        self.m_buffer[l_offset].copy(p_quart)

    def readBuffer(self, p_offset = 0):
        l_offset = p_offset % len(self.m_buffer)
        return self.m_buffer[l_offset]

    def getQueue(self):
        return self.m_queue

    def addQueue(self, p_chunk):
        l_chunk = Chunk(p_chunk.getID())
        l_chunk.copy(p_chunk)
        self.m_queue.append(l_chunk)

    def movePC(self, p_value):
        self.m_wo += p_value
        self.m_pc = (self.m_pc + p_value) % const.MEMORY_SIZE

    def getRegister(self, p_idx):
        return self.m_registers[p_idx]
    def getMode(self):
        return self.m_mode
    def getZ(self):
        return self.m_z
    def getS(self):
        return self.m_s
    def getPC(self):
        return self.m_pc
    def getInitialPC(self):
        return self.m_initialPC
    def getID(self):
        return self.m_id
    def getOwner(self):
        return self.m_owner
    def getComment(self):
        return self.m_comment
    def getWO(self):
        return self.m_wo
    def getLastCheckCycle(self):
        return self.m_lastCheckCycle
    def getLastCheckWO(self):
        return self.m_lastCheckWO
    def getForkState(self):
        return self.m_forkState
    def getCheckState(self):
        return self.m_checkState
    def getCurrentInstr(self):
        return self.m_instr
    def getDecodeDelay(self):
        return self.m_decodeDelay
    def getExecuteDelay(self):
        return self.m_executeDelay
    def getNbCycle(self):
        return self.m_nbCycle

    def setInstr(self, p_instr):
        self.m_instr = p_instr
        self.m_queue = []

    def setOwner(self, p_owner):
        self.m_owner = p_owner
    def setComment(self, p_comment):
        self.m_comment = p_comment
    def setMode(self, p_mode):
        self.m_mode = p_mode
    def setPC(self, p_value):
        self.m_pc = p_value
    def setInitialPC(self, p_value):
        self.m_initialPC = p_value
    def setZ(self, p_state):
        self.m_z = p_state
    def setS(self, p_state):
        self.m_s = p_state
    def setForkState(self, p_state):
        self.m_forkState = p_state
    def setCheckState(self, p_state):
        self.m_checkState = p_state
    def setLastCheckCycle(self, p_value):
        self.m_lastCheckCycle = p_value
    def setLastCheckWO(self, p_value):
        self.m_lastCheckWO = p_value
    def setDecodeDelay(self, p_delay):
        self.m_decodeDelay = p_delay
    def setExecuteDelay(self, p_delay):
        self.m_executeDelay = p_delay
    def setNbCycle(self, p_val):
        self.m_nbCycle = p_val
    def isReadingState(self):
        return self.m_state == Ship.States.Reading
    def isDecodingState(self):
        return self.m_state == Ship.States.Decoding
    def isExecutingState(self):
        return self.m_state == Ship.States.Executing

    def getStatus(self):
        if   self.m_status == Ship.Status.Disqualified: return "Disqualified"
        elif self.m_status == Ship.Status.Running:      return "Running"
        elif self.m_status == Ship.Status.Winner:       return "Winner"
        elif self.m_status == Ship.Status.Dead:         return "Dead"
        elif self.m_status == Ship.Status.Crashed:      return "Crashed"

    def isRunningStatus(self):
        return (self.m_status == Ship.Status.Running)
    def isWinnerStatus(self):
        return (self.m_status == Ship.Status.Winner)
    def isDeadStatus(self):
        return (self.m_status == Ship.Status.Dead)

    def setDisqualified(self):
        self.m_status = Ship.Status.Disqualified
    def setWinner(self):
        self.m_status = Ship.Status.Winner
    def setDead(self):
        self.m_status = Ship.Status.Dead
    def setCrashed(self):
        self.m_status = Ship.Status.Crashed
    def setReadingState(self):
        self.m_state = Ship.States.Reading
    def setDecodingState(self):
        self.m_state = Ship.States.Decoding
    def setExecutingState(self):
        self.m_state = Ship.States.Executing
