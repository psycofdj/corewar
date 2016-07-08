# -*- coding: utf-8
#---------------------------------------------------------------------------#

import re
from pyscript.exceptions    import SqlExecuteException
from pyscript.sql.handler   import sqlDefaultHandler, makeSqlConfig, autocommit, autoconnect
from pyscript               import config
from corewar.core.data.ship import Ship as VmShip

#---------------------------------------------------------------------------#

class Ship(sqlDefaultHandler):
    def __init__(self):
        l_config = makeSqlConfig(config.get("mysql", "username"),
                                 config.get("mysql", "password"),
                                 config.get("mysql", "host"),
                                 config.get("mysql", "database"))
        sqlDefaultHandler.__init__(self, l_config)


    def __getNameFromCode(self, p_code):
        l_match = re.search(".name +\"([^\"]+)\"", p_code, re.MULTILINE)
        if not l_match:
            return None;
        return l_match.groups()[0]

    @autoconnect
    @autocommit
    def getByID(self, p_id):
        return self.selectFirst(["*"], "ship", {"id" : int(p_id)})

    @autoconnect
    @autocommit
    def listByUserID(self, p_uid):
        l_query = "SELECT * from ship join user_ship on ship.id = user_ship.sid where user_ship.uid = %s" % self.quoteItem(p_uid)
        return self.execute(l_query);

    @autoconnect
    @autocommit
    def getByUserShipID(self, p_uid, p_sid):
        l_query = "SELECT * from ship join user_ship on ship.id = user_ship.sid where user_ship.uid = %s and user_ship.sid = %s" % (self.quoteItem(p_uid), self.quoteItem(p_sid))
        l_data  = self.execute(l_query);
        if len(l_data):
            return l_data[0]
        return None

    @autoconnect
    @autocommit
    def updateShip(self, p_uid, p_shipID, p_shipCode, p_compiles):
        l_name = self.__getNameFromCode(p_shipCode)
        if not l_name:
            return ["noname"]
        l_data = {
            "name"     : l_name,
            "date"     : "NOW()",
            "compiles" : p_compiles,
            "code"     : p_shipCode }
        l_cond = { "id" : p_shipID }
        try:
            self.update(l_data, "ship", l_cond)
            return []
        except SqlExecuteException, l_error:
            if l_error.m_sqlError.args[0] == 1062: #duplicate key
                return ["duplicate"]
            raise l_error

    @autoconnect
    @autocommit
    def createShip(self, p_uid, p_shipCode, p_compiles):
        l_name = self.__getNameFromCode(p_shipCode)
        if not l_name:
            return 0, ["noname"]

        l_data = {
            "name"     : l_name,
            "date"     : "NOW()",
            "compiles" : p_compiles,
            "code"     : p_shipCode }
        try:
            l_id = self.insert(l_data, "ship")
        except SqlExecuteException, l_error:
            if l_error.m_sqlError.args[0] == 1062: #duplicate key
                return 0, ["duplicate"]
            raise l_error

        l_data = {
            "uid" : p_uid,
            "sid" : l_id }
        self.insert(l_data, "user_ship")
        return l_id, []

    @autoconnect
    @autocommit
    def deleteShip(self, p_shipID):
        l_query = "DELETE from ship WHERE id=%s" % self.quoteItem(p_shipID)
        self.execute(l_query)

    @autoconnect
    @autocommit
    def raceResultExists(self, p_uid, p_ship):
        l_cols = ["id"]
        l_cond = {
            "uid"  : p_uid,
            "hash" : "SHA2(%s, 256)" % self.quoteItem(p_ship["code"])
            }
        l_result = self.select(l_cols, "time_results", l_cond)
        return len(l_result) > 0

    @autoconnect
    @autocommit
    def createRaceResult(self, p_uid, p_ship, p_vmShip, p_logs):
        l_data = {
            "uid"      : p_uid,
            "name"     : p_ship["name"],
            "code"     : p_ship["code"],
            "hash"     : "SHA2(%s, 256)" % self.quoteItem(p_ship["code"]),
            "log"      : "\n".join(p_logs),
            "finished" : 0,
            "cycles"   : p_vmShip.getNbCycle(),
            "date"     : "NOW()" }

        if str(p_vmShip.getStatus()) == "Winner":
            l_data["finished"] = 1

        try:
            self.insert(l_data, "time_results")
        except SqlExecuteException, l_error:
            if l_error.m_sqlError.args[0] == 1062: #duplicate key
                return ["duplicate"]
            raise l_error
        return []
