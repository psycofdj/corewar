 # -*-coding:UTF-8 -*
#---------------------------------------------------------------------------#

import cherrypy

from pyscript                      import config
from pyscript.tools.sendmail       import send_mail
from pyscript.tools.randomgen      import gen_password
from corewar.webserver.page        import GenericPage
from corewar.webserver.models.user import User

#---------------------------------------------------------------------------#

class Page(GenericPage):
    def __init__(self, p_app):
        GenericPage.__init__(self, p_app)

    @cherrypy.expose
    def login(self, p_mail = None, p_password = None, p_dest = "/"):
        l_userModel = User()
        l_param = {
            "p_mail"     : p_mail,
            "p_password" : p_password,
            "p_dest"     : p_dest }
        if p_mail and p_password:
            l_user  = l_userModel.getByMailPass(p_mail, p_password)
            if l_user != None:
                cherrypy.session['uid'] = l_user["id"]
                return self.redirect(p_dest)
            l_param["error"] = True
        return self.serveContent("user/login.tpl", **l_param)

    @cherrypy.expose
    def register(self, p_name = None, p_nickname = None, p_mail = None, p_password = None):
        l_userModel = User()
        l_errors = {}
        if p_name and p_nickname and p_mail and p_password:
            l_errors = l_userModel.create(p_name, p_nickname, p_mail, p_password)
            if len(l_errors) == 0:
                return self.redirect("/user/login")
        return self.serveContent("user/register.tpl", **l_errors)

    @cherrypy.expose
    def recover(self, p_mail = None):
        l_userModel = User()
        l_errors = {}
        if p_mail:
            l_user = l_userModel.getByMail(p_mail)
            if l_user != None:
                l_mail = l_user["mail"]
                l_newPass = gen_password(8)
                l_userModel.updatePassword(p_mail, l_newPass)
                send_mail(p_mail,
                          "Corewar : génération de mot de passe",
                          "Le nouveau mot de passe associé à cette adresse est : %s" % l_newPass,
                          config.get("mail", "from"),
                          config.get("mail", "host"),
                          config.get("mail", "port"))
                l_errors["sent"] = True
            else:
                l_errors["unknown"] = True
        return self.serveContent("user/recover.tpl", **l_errors)

    @cherrypy.expose
    def logout(self, **kwds):
        cherrypy.session.pop('uid')
        return self.redirect("/user/login")

    @cherrypy.expose
    def index(self):
        return self.serveContent("rules/index.tpl")
