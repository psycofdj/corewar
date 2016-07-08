# -*- coding: utf-8
#---------------------------------------------------------------------------#

from pyscript             import config
from pyscript.exceptions  import SqlExecuteException
from pyscript.sql.handler import sqlDefaultHandler, makeSqlConfig, autocommit, autoconnect

#---------------------------------------------------------------------------#

class User(sqlDefaultHandler):
    def __init__(self):
        l_config = makeSqlConfig(config.get("mysql", "username"),
                                 config.get("mysql", "password"),
                                 config.get("mysql", "host"),
                                 config.get("mysql", "database"))
        sqlDefaultHandler.__init__(self, l_config)

    @autoconnect
    @autocommit
    def getByID(self, p_id):
        l_cols  = ["*"]
        l_conds = {"id" : p_id}
        return self.selectFirst(l_cols, "user", l_conds)

    @autoconnect
    @autocommit
    def getByMailPass(self, p_mail, p_pass):
        l_cols  = ["*"]
        l_conds = { "mail"     : p_mail,
                    "password" : "SHA2(%s, 512)" % self.quoteItem(p_pass) }
        return self.selectFirst(l_cols, "user", l_conds)

    @autoconnect
    @autocommit
    def getByMail(self, p_mail):
        l_cols  = ["*"]
        l_conds = {"mail" : p_mail}
        return self.selectFirst(l_cols, "user", l_conds)

    @autoconnect
    @autocommit
    def updatePassword(self, p_mail, p_newPass):
        l_data = { "password" : "SHA2(%s, 512)" % self.quoteItem(p_newPass) }
        l_cond = { "mail"     : p_mail }
        self.update(l_data, "user", l_cond)

    @autoconnect
    @autocommit
    def create(self, p_name, p_nickname, p_mail, p_password):
        l_data = {
            "name"     : p_name,
            "nickname" : p_nickname,
            "mail"     : p_mail,
            "password" : 'SHA2(%s, 512)' % self.quoteItem(p_password) }

        try:
            self.insert(l_data, "user")
            return {}
        except SqlExecuteException, l_error:
            if l_error.m_sqlError.args[0] == 1062: #duplicate key
                return { "duplicate" : True }
            raise l_error
