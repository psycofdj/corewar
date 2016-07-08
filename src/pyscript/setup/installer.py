#!/usr/bin/python -OO
# -*-coding:UTF-8 -*
#-----------------------------------------------------------------------------#

import re
import os
import sys
import getpass
import stat
import subprocess
import shutil
import pwd

#-----------------------------------------------------------------------------#

from pyscript.sql.handler import sqlDefaultHandler
from pyscript import config
from pyscript.exceptions import SetupException

#from ngstream.core.lib.configuration.parser import _resolve

#-----------------------------------------------------------------------------#

class BaseInstaller:
    def __init__(self, p_options, p_name, p_targetConfig, p_sqlConfig):
        self.m_targetConfig = p_targetConfig
        self.m_options = p_options
        self.m_name = p_name
        self.m_sql = sqlDefaultHandler(p_sqlConfig)
        self.m_sqlSuperUser = config.get("mysql", "username")
        self.m_sqlSuperPasswd = config.get("mysql", "password")
        self.m_dependencies = []
        self.m_reverseDep = []
        self.m_installFunc = []
        self.m_uninstallFunc = []

    def initialize(self):
        raise NotImplemented

    def finalize(self):
        raise NotImplemented

    def registerInstall(self, p_func):
        self.m_installFunc.append(p_func)

    def registerUninstall(self, p_func):
        self.m_uninstallFunc.append(p_func)

    def require(self, p_moduleName):
        self.m_dependencies.append(p_moduleName)

    def rm(self, p_filePath, p_failIfNotExist = True):
        if not os.path.isfile(p_filePath):
            if p_failIfNotExist :
                raise SetupException("could not delete unexisting file '%s'" % p_filePath)
        else:
            os.unlink(p_filePath)

    def rmdir(self, p_path, p_empty = True):
        if not p_empty:
            shutil.rmtree(p_path)
        else:
            for c_entry in os.listdir(p_path):
                if os.path.isdir(os.path.join(p_path, c_entry)):
                    self.rmdir(os.path.join(p_path, c_entry), l_empty)
            if not len(os.listdir(p_path)):
                shutil.rmtree(p_path)

    def checkRoot(self):
        if os.getuid() != 0:
            raise SetupException("you must be root to run setup script")

    def getReverseDeps(self):
        if not os.path.exists('setup/.module.%s' % self.m_name):
            return []
        l_file = open('setup/.module.%s' % self.m_name, "r")
        l_rep = []
        for c_line in l_file:
            l_rep.append(c_line.split()[0])
        l_file.close()
        return l_rep

    def sqlMagicConnect(self):
        try:
            self.m_sql.connect()
            return False
        except:
            self.sqlAdminConnect()
            return True

    def sqlAdminConnect(self):
            self.getSqlAdmin()
            self.m_sql.connect(p_user=self.m_sqlSuperUser, p_passwd=self.m_sqlSuperPasswd)

    def getSqlAdmin(self):
        if self.m_sqlSuperUser == None:
            l_cmd = 'dialog --backtitle "Installation" --keep-window --inputbox "Enter MySql admin login" 10 40 root'
            l_process = subprocess.Popen(l_cmd, shell=True, stderr=subprocess.PIPE)
            l_process.wait()
            self.m_sqlSuperUser = l_process.stderr.readline()
            if self.m_sqlSuperUser == "":
                self.m_sqlSuperUser = "root"
            print ""

        if self.m_sqlSuperPasswd == None:
            l_cmd = 'dialog --backtitle "Installation" --keep-window  --passwordbox "Enter MySql password for [root]" 10 40'
            l_process = subprocess.Popen(l_cmd, shell=True, stderr=subprocess.PIPE)
            l_process.wait()
            self.m_sqlSuperPasswd = l_process.stderr.readline()
            print ""

    def dialogYesNo(self, p_message, p_title = "Installation", p_width = 40, p_height = 10):
        l_cmd = 'dialog --backtitle "%s" --keep-window  --yesno "%s" "%d" "%d"'
        l_cmd = l_cmd % (p_title, p_message, p_height, p_width)
        return os.system(l_cmd) == 0

    def confirmDeleteDirectory(self, p_directoryPath, p_message):
        if os.path.isdir(p_directoryPath):
            l_message = "%s\n%s" % (p_message, p_directoryPath)
            if self.dialogYesNo(l_message, p_width = len(p_directoryPath) + 9, p_height=7):
                self.rmdir(p_directoryPath, empty=False)

    def writeReverseDep(self, p_dep):
        l_file = open('setup/.module.%s' % p_dep, "r")
        for c_line in l_file:
            l_module = c_line.split()[0]
            if l_module == self.m_name:
                l_file.close()
                return False
        l_file.close()
        l_file = open('setup/.module.%s' % p_dep, "a")
        l_file.write("%s\n" % self.m_name)
        l_file.close()


    def removeReverseDep(self, p_dep):
        l_file = open('setup/.module.%s' % p_dep, "r")
        l_content = l_file.readlines()
        l_file.close()
        l_file = open('setup/.module.%s' % p_dep, "w")
        for c_line in l_content:
            if c_line.split()[0] != self.m_name:
                l_file.write(c_line)
        l_file.close()

    def install(self, p_force = False):
        if not os.path.exists('setup/.module.%s' % self.m_name) or p_force:
            print "... installing module %s" % self.m_name
            for c_func in self.m_installFunc:
                c_func()
            for c_dep in self.m_dependencies:
                self.writeReverseDep(c_dep)
            open('setup/.module.%s' % self.m_name, "a").close()

    def uninstall(self, p_force = False):
        if os.path.exists('setup/.module.%s' % self.m_name) or p_force:
            print "... uninstalling module %s" % self.m_name
            for c_func in self.m_uninstallFunc:
                c_func()
            for c_dep in self.m_dependencies:
                self.removeReverseDep(c_dep)
            os.unlink('setup/.module.%s' % self.m_name)

    def reinstall(self):
        self.uninstall()
        self.install()

    def expand(self, p_str):
        l_finder = re.compile("\$\{([^}]+)\}")
        l_variables = l_finder.findall(p_str)
        l_str = p_str
        for c_varName in l_variables:
            l_namespaces = c_varName.split(":")
            l_dico = self.m_targetConfig
            for c_namespace in l_namespaces:
                if not c_namespace in l_dico:
                    raise SetupException("unable to resolve variable '%s' fron config" % c_varName)
                l_dico = l_dico[c_namespace]
            l_str = l_str.replace("${%s}" % c_varName, l_dico)
        return l_str

    def executeScript(self, p_scriptPath):
        l_file = open(p_scriptPath, "r")
        l_buf = ""
        for c_line in l_file:
            l_buf += c_line
        l_buf = self.expand(l_buf)
        self.m_sql.execute(l_buf)

    def mkdir(self, p_directoryPath):
        if not os.path.isdir(p_directoryPath):
            l_cmdLine = []
            l_cmdLine.append("mkdir")
            l_cmdLine.append("-p")
            l_cmdLine.append(p_directoryPath)
            if os.system(" ".join(l_cmdLine)):
                raise SetupException("could not create directory : %s" % p_directoryPath)

    def getApacheUserInfo(self):
        l_apacheUserName = ""
        l_apacheEnvFilePath = "/etc/apache2/envvars"
        try:
            l_apacheEnvFile = open("/etc/apache2/envvars", "r")
        except:
            raise BaseException("could not open apache file '%s'" % l_apacheEnvFilePath)

        for l_line in l_apacheEnvFile.readlines():
            l_matches = re.findall("^.*APACHE_RUN_USER *= *([^ ]+).*\n$", l_line)
            if len(l_matches):
                l_apacheUserName = l_matches[0]
        l_apacheEnvFile.close()

        if l_apacheUserName == "":
            raise BaseException("could not find apache user name in '%s'" % l_apacheEnvFilePath)

        try:
            return pwd.getpwnam(l_apacheUserName)
        except:
            raise BaseException("could not find user '%s' in unix user database" % l_apacheUserName)


    def setGroup(self, p_filePath, p_groupID):
        l_fileStat = os.stat(p_filePath)
        try:
            os.chown(p_filePath, l_fileStat.st_uid, p_groupID)
        except:
            raise BaseException("could not set group '%s' on '%s'" % (p_groupID, p_filePath))

    def setGroupWritable(self, p_filePath):
        l_fileMode = os.stat(p_filePath)[stat.ST_MODE]
        l_newFileMode = (l_fileMode | stat.S_IWGRP)
        try:
            os.chmod(p_filePath, l_newFileMode)
        except:
            raise Exception, "could not give group write permissions to '%s'" % p_filePath

    def setWritable(self, p_filePath):
        l_fileMode = os.stat(p_filePath)[stat.ST_MODE]
        l_newFileMode = (l_fileMode | stat.S_IWUSR)
        try:
            os.chmod(p_filePath, l_newFileMode)
        except:
            raise BaseException("could not give group write permissions to '%s'" % p_filePath)

    def touch(self, p_fileName, p_createParentDir = True):
        if p_createParentDir:
            l_parentDirPath = os.path.dirname(p_fileName);
            if len(l_parentDirPath):
                self.mkdir(l_parentDirPath)
        try:
            l_createdFile = open(p_fileName, "w+")
            l_createdFile.close()
        except:
            raise BaseException, "could not create file '%s'" % p_fileName

    def linkCronScript(self, p_script, p_mode):
        l_dest = os.path.join("scripts", "cron")
        l_dest = os.path.join(l_dest, "cron.%s" % p_mode)
        l_path, l_ext = os.path.splitext(p_script)
        l_dest = os.path.join(l_dest, l_path)
        l_dest = os.path.abspath(l_dest)
        if not os.path.exists(l_dest):
            print "... [%s] installing cron script" % self.m_name
            l_src = os.path.join("scripts", p_script)
            l_src = os.path.abspath(l_src)
            os.symlink(l_src, l_dest)

    def unlinkCronScript(self, p_script, p_mode):
        l_dest = os.path.join("scripts", "cron")
        l_dest = os.path.join(l_dest, "cron.%s" % p_mode)
        l_path, l_ext = os.path.splitext(p_script)
        l_dest = os.path.join(l_dest, l_path)
        if os.path.exists(l_dest):
            print "... [%s] uninstalling cron script" % self.m_name
            os.unlink(l_dest)

    def stopService(self, p_serviceName, p_failIsError = True):
        if os.system("service %s stop >/dev/null" % p_serviceName) and p_failIsError:
            raise BaseException("could not stop linux service '%s'" % p_serviceName)

    def startService(self, p_serviceName, p_failIsError = True):
        if os.system("service %s start  >/dev/null" % p_serviceName) and p_failIsError:
            raise BaseException("could not start linux service '%s'" % p_serviceName)

    def restartService(self, p_serviceName, p_failIsError = True):
        self.stopService(p_serviceName, p_failIsError)
        self.startService(p_serviceName, p_failIsError)

#-----------------------------------------------------------------------------#
