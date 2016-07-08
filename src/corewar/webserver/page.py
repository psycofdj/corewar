# -*-coding:UTF-8 -*
#---------------------------------------------------------------------------#

import cherrypy

from mako.template import Template
from mako.lookup import TemplateLookup
import json
#---------------------------------------------------------------------------#


def logged_serve(p_template, p_params):
    def decorate(p_func):
        def wrapper(self, *p_args, **p_kwds):
            if not self.isLogged():
                return p_page.serveContent(p_template, p_params)
            return p_func(self, *p_args, **p_kwds)
        return wrapper
    return decorate

def logged_redirect(p_dest = "/"):
    def decorate(p_func):
        def wrapper(self, *p_args, **p_kwds):
            if not self.isLogged():
                return self.redirect(p_dest)
            p_kwds["p_uid"] = cherrypy.session["uid"]
            return p_func(self, *p_args, **p_kwds)
        return wrapper
    return decorate


class GenericPage:
    def __init__(self, p_app):
        self.m_app = p_app
        self.m_lookup = TemplateLookup(directories     = ["templates"],
                                       output_encoding = "utf-8",
                                       input_encoding  = "utf-8",
                                       default_filters = ['decode.utf8'])


    def serveJson(self, p_data):
        cherrypy.response.headers['Content-Type'] = "application/json; charset=utf-8"
        return json.dumps(p_data)

    def serveText(self, p_data):
        cherrypy.response.headers['Content-Type'] = "text/plain; charset=utf-8"
        return p_data

    def serveFile(self, p_fileName, p_fileData):
        cherrypy.response.headers['Content-Type']        = "text/plain; charset=utf-8"
        cherrypy.response.headers['Content-Disposition'] = "attachment; filename=\"%s\"" % p_fileName
        return p_fileData

    def serveTemplate(self, p_fileName, *args, **kwds):
        cherrypy.response.headers['Content-Type'] = "text/html; charset=utf-8"
        l_tmpl = self.m_lookup.get_template(p_fileName)
        kwds['app']    = self. m_app
        kwds['logged'] = self.isLogged()
        return l_tmpl.render(*args, **kwds)

    def serveContent(self, p_fileName, *args, **kwds):
        cherrypy.response.headers['Content-Type'] = "text/html; charset=utf-8"
        l_tmpl = self.m_lookup.get_template("index.tpl")

        kwds['app']    = self. m_app
        kwds['page']   = p_fileName
        kwds['logged'] = self.isLogged()
        return l_tmpl.render(*args, **kwds)

    def redirect(self, p_dest):
        raise cherrypy.HTTPRedirect(p_dest)

    def getApp(self):
        return self.m_app

    def isLogged(self):
        return "uid" in cherrypy.session
