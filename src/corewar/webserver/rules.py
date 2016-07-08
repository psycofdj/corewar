# -*- coding: utf-8
#---------------------------------------------------------------------------#

import cherrypy

from corewar.webserver.page import GenericPage

#---------------------------------------------------------------------------#

class Page(GenericPage):
    def __init__(self, p_app):
        GenericPage.__init__(self, p_app)

    @cherrypy.expose
    def instructions(self):
        return self.serveContent("rules/faq.tpl")

    @cherrypy.expose
    def instructions(self):
        return self.serveContent("rules/instructions.tpl")

    @cherrypy.expose
    def vm(self):
        return self.serveContent("rules/vm.tpl")

    @cherrypy.expose
    def language(self):
        return self.serveContent("rules/language.tpl")

    @cherrypy.expose
    def league(self):
        return self.serveContent("rules/league.tpl")

    @cherrypy.expose
    def faq(self):
        return self.serveContent("faq.tpl")

    @cherrypy.expose
    def index(self):
        return self.serveContent("rules/index.tpl")
