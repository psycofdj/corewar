# -*- coding: utf-8 -*
#---------------------------------------------------------------------------#

import cherrypy

from corewar.webserver.page          import GenericPage, logged_serve, logged_redirect
from corewar.webserver.models.league import League

#---------------------------------------------------------------------------#

class Page(GenericPage):
    def __init__(self, p_app):
        GenericPage.__init__(self, p_app)

    @cherrypy.expose
    def time_attack(self):
        l_leagueModel = League()
        l_params      = {}
        l_params["results"] = l_leagueModel.getResults()

        l_params["p_uid"] = None
        if self.isLogged():
          l_params["p_uid"] = cherrypy.session["uid"]
        return self.serveContent("/league/time_attack.tpl", **l_params)


    @cherrypy.expose
    @logged_redirect("/league/time_attack")
    def log(self, p_uid, p_rid):
        l_leagueModel = League()
        l_result      = l_leagueModel.getByID(p_rid)
        if l_result["uid"] != p_uid:
            self.redirect("/league/time_attack")
        l_fileData    = l_result["log"]
        l_fileName    = "log.txt"
        return self.serveFile(l_fileName, l_fileData)

    @cherrypy.expose
    def index(self):
        return self.redirect("/league/time_attack")
