# -*- coding: utf-8 -*
#---------------------------------------------------------------------------#

import cherrypy
import copy
import time
from threading import Thread
from corewar.core.vm import VirtualMachine
from corewar.core.pit.pit import Pit
from corewar.webserver.page import GenericPage, logged_serve, logged_redirect
from corewar.webserver.models.ship import Ship

#---------------------------------------------------------------------------#


class VMThread(Thread):
    def __init__(self, p_shipCode, p_logModes):
        Thread.__init__(self)
        self.m_resultStr = ""
        self.m_result    = None
        self.m_vm = VirtualMachine(VirtualMachine.League.Race, p_logModes)
        self.m_vm.addShipCode(p_shipCode)

    def getLogs(self):
        return self.m_vm.getLogs()
    def getResultStr(self):
        return self.m_resultStr
    def getBest(self):
        return self.m_vm.filterResults(self.m_result, "best")[0]
    def getData(self):
        return {
            "init" : self.m_vm.m_dataInit,
            "cycles" : self.m_vm.m_dataCycle,
            "finish" : self.m_vm.m_dataFinish
        }
    def run(self):
        self.m_vm.initialize()
        self.m_result    = self.m_vm.run()
        self.m_resultStr = self.m_vm.printResult(self.m_result)

def race(p_shipCode, p_logModes):
    l_lastLog = 0
    l_thread  = VMThread(p_shipCode, p_logModes)
    l_thread.start()
    while l_thread.isAlive():
        l_curLog = len(l_thread.getLogs())
        if l_curLog == l_lastLog:
            time.sleep(1)
            continue
        l_data = l_thread.getLogs()[l_lastLog:l_curLog]
        l_lastLog = l_curLog
        yield "\n".join(l_data) + "\n"
    l_curLog = len(l_thread.getLogs())
    if l_curLog != l_lastLog:
        l_data = l_thread.getLogs()[l_lastLog:l_curLog]
        yield "\n".join(l_data) + "\n"
    yield l_thread.getResultStr()


class Page(GenericPage):
    def __init__(self, p_app):
        GenericPage.__init__(self, p_app)

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def edit(self, p_uid, p_shipID = None):
        l_shipModel = Ship()
        l_params = { "ship" : None }
        if p_shipID:
            l_params["ship"] = l_shipModel.getByUserShipID(p_uid, p_shipID)
        return self.serveContent("/pit/edit.tpl", **l_params)

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def save(self, p_uid, p_shipCode, p_shipID) :
        l_shipModel = Ship()
        l_pit      = Pit()
        l_ship     = l_shipModel.getByUserShipID(p_uid, p_shipID);

        p_shipCode = p_shipCode.strip()
        l_pit.buildShipCode(p_shipCode)
        l_messages = l_pit.getLogs()
        l_compiles = 1
        if l_pit.hasError():
            l_compiles = 0

        if l_ship:
            l_shipID = p_shipID
            l_errors = l_shipModel.updateShip(p_uid, p_shipID, p_shipCode, l_compiles)
        else:
            l_shipID, l_errors = l_shipModel.createShip(p_uid, p_shipCode, l_compiles)

        return self.serveJson({ "id" : l_shipID, "errors" : l_errors, "messages" : l_messages })

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def compile(self, p_uid, p_shipCode) :
        l_pit = Pit()
        l_pit.buildShipCode(p_shipCode)
        l_messages = l_pit.getLogs()
        return self.serveJson({ "messages" : l_messages })

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def list(self, p_uid):
        l_shipModel = Ship()
        l_params = {
            "ships"  : l_shipModel.listByUserID(p_uid),
            "errors" : []
        }
        return self.serveContent("/pit/list.tpl", **l_params)

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def delete(self, p_uid, p_shipID):
        l_shipModel = Ship()
        l_shipModel.deleteShip(p_shipID)
        return self.redirect("/pit/list")

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def run(self, p_uid, **p_kwds):
        l_shipModel = Ship()
        p_kwds["ship"] = l_shipModel.getByID(p_kwds["shipID"])
        if not "run" in p_kwds:
            return self.serveContent("/pit/run.tpl", **p_kwds)
        l_logs = [ x for x,y in p_kwds.items() if y == "checked" ]
        return race(p_kwds["ship"]["code"].decode("utf-8"), l_logs)

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/list")
    def run_gui(self, p_uid, **p_kwds):
        l_shipModel = Ship()
        l_ship      = l_shipModel.getByID(p_kwds["shipID"]);
        l_runThread = VMThread(l_ship["code"].decode("utf-8"), None)
        l_runThread.start()
        l_runThread.join()
        p_kwds["data"] = l_runThread.getData();
        return self.serveTemplate("/pit/gui.tpl", **p_kwds)

    @cherrypy.expose
    @logged_redirect("/user/login?p_dest=/pit/run")
    def apply(self, p_uid, p_shipID, p_leagueType):
        l_shipModel = Ship()
        if p_leagueType != "time":
            return self.redirect("/pit/list")
        l_params    = {}
        l_ship      = l_shipModel.getByID(p_shipID)
        if l_shipModel.raceResultExists(p_uid, l_ship):
            l_params["errors"] = ["duplicate"]
            l_params["ships"] = l_shipModel.listByUserID(p_uid)
            return self.serveContent("/pit/list.tpl", **l_params)

        l_shipCode  = l_ship["code"].decode("utf-8")
        l_runThread = VMThread(l_shipCode, None)
        l_runThread.start()
        l_runThread.join()
        l_vmShip    = l_runThread.getBest()
        l_logs      = l_runThread.getLogs()
        l_params["errors"] = l_shipModel.createRaceResult(p_uid, l_ship, l_vmShip, l_logs)
        if l_params["errors"]:
            l_params["ships"] = l_shipModel.listByUserID(p_uid)
            return self.serveContent("/pit/list.tpl", **l_params)

        return self.redirect("/league/time_attack")

    @cherrypy.expose
    def index(self):
        return self.redirect("/pit/list")

