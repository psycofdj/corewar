# -*- coding: utf-8

import os
import corewar
from pyscript.setup.installer import BaseInstaller
from pyscript import config
from pyscript.sql.handler import makeSqlConfig

#-----------------------------------------------------------------------------#

def getModuleConfig():
    corewar.GLOBAL_CONFIG["__internal"]["action"] = "start"
    l_getter = config.init_file_config(corewar.GLOBAL_CONFIG,
                                       "corewar.cfg",
                                       corewar.validation_handler)
    return l_getter

class Installer(BaseInstaller):
    def __init__(self, p_options = None):
        self.get = getModuleConfig()
        l_config = makeSqlConfig(self.get("mysql", "username"),
                                 self.get("mysql", "password"),
                                 self.get("mysql", "host"))
        BaseInstaller.__init__(self, p_options, "corewar", corewar.GLOBAL_CONFIG, l_config)
        self.registerInstall(self.install_perm)
        self.registerInstall(self.install_sql)
        if not config.get("general", "keep"):
            self.registerUninstall(self.uninstall_sql)
        self.registerUninstall(self.uninstall_files)

    def initialize(self):
        pass

    def finilize(self):
        pass

    def install_perm(self):
        print "... [corewar] creating files and directories"
        self.touch(self.get("log", "file"))
        self.touch(self.get("web", "pid-file"))
        print "... [corewar] setting up permissions"
        self.setWritable(self.get("log", "file"))
        self.setWritable(self.get("web", "pid-file"))

    def install_sql(self):
        l_db = self.expand("${mysql:database}")
        l_admin = self.sqlMagicConnect()
        if not self.m_sql.hasDatabase(l_db):
            print "... [corewar] installing sql database"
            if not l_admin:
                self.m_sql.disconnect()
                self.sqlAdminConnect()
                l_admin = True
            self.executeScript("setup/corewar/sql/create_database.sql")

        if not self.m_sql.hasTable("user", l_db):
            print "... [corewar] installing sql user table and data"
            self.executeScript("setup/corewar/sql/create_user.sql")

        if not self.m_sql.hasTable("ship", l_db):
            print "... [corewar] installing sql ship table and data"
            self.executeScript("setup/corewar/sql/create_ship.sql")

        if not self.m_sql.hasTable("time_results", l_db):
            print "... [corewar] installing sql time_results table"
            self.executeScript("setup/corewar/sql/create_league.sql")

        if not self.m_sql.hasUser(self.expand('${mysql:username}')):
            print "... [corewar] installing sql user"
            if not l_admin:
                self.m_sql.disconnect()
                self.sqlAdminConnect()
                admin = True
            self.executeScript("setup/corewar/sql/create_sqluser.sql")
        self.m_sql.disconnect()

    def uninstall_sql(self):
        l_admin = self.sqlAdminConnect()
        l_db = self.expand("${mysql:database}")

        print "... [corewar] dropping sql tables"
        self.executeScript("setup/corewar/sql/drop_tables.sql")

        if self.m_sql.hasDatabase(l_db):
            print "... [corewar] uninstalling database"
            self.executeScript("setup/corewar/sql/drop_database.sql")

        if self.m_sql.hasUser(self.expand('${mysql:username}')) and self.expand('${mysql:username}') != "root":
            print "... [corewar] uninstalling sql user"
            self.executeScript("setup/corewar/sql/drop_sqluser.sql")
        self.m_sql.disconnect()

    def uninstall_files(self):
        print "... [corewar] deleting files and directories"
        self.rm(self.get("log", "file"))

#-----------------------------------------------------------------------------#
