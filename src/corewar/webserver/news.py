# -*- coding: utf-8
#---------------------------------------------------------------------------#

import cherrypy

from corewar.webserver.page import GenericPage

#---------------------------------------------------------------------------#

class Page(GenericPage):
    def __init__(self, p_app):
        GenericPage.__init__(self, p_app)

    @cherrypy.expose
    def index(self):
        return self.serveContent("news.tpl")
