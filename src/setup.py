#!/usr/bin/python -O
# -*-coding:UTF-8 -*
#---------------------------------------------------------------------------#

import time
import sys
import os
import signal
import time

import setup

from pyscript import exceptions
from pyscript import config
from pyscript.config import init_config

#------------------------------------------------------------------------------#

def moduleExists(p_moduleName):
    if not os.path.isdir(os.path.join("setup", p_moduleName)):
        return False
    if not os.path.isfile(os.path.join(os.path.join("setup", p_moduleName), "__init__.py")):
        return False
    return True

#---------------------------------------------------------------------------#

def moduleImport(p_moduleName):
    l_module = __import__("setup.%s" % p_moduleName)
    l_module = getattr(l_module, p_moduleName)
    l_module.m_name = p_moduleName
    return l_module

#---------------------------------------------------------------------------#

def mergeDict(p_d1, p_d2):
    l_rep = {}
    for c_d1k in p_d1.keys():
        l_rep[c_d1k] = p_d1[c_d1k]
    for c_d2k in p_d2.keys():
        l_rep[c_d2k] = p_d2[c_d2k]
    return l_rep

#---------------------------------------------------------------------------#

def checkCircularReference(p_tested, p_modules, p_module, p_tmp):
    if not p_module.m_name in p_tmp:
        p_tmp.append(p_module.m_name)
    for c_dep in p_module.installer.m_dependencies:
        if (c_dep in p_tmp) and (c_dep == p_tested):
            print "error : cirucular dependency between modules %s and %s" % (p_module.m_name, c_dep)
            sys.exit(1)
        else:
            p_tmp.append(c_dep)
        checkCircularReference(p_tested, p_modules, p_modules[c_dep], p_tmp)
    return p_tmp

#---------------------------------------------------------------------------#

def execute(p_modules, p_arg, p_method, p_force):
    if (p_method == "install"):
        for c_dep in p_modules[p_arg].installer.m_dependencies:
            execute(p_modules, c_dep, p_method, p_force)

    if (p_method == "uninstall"):
        for c_dep in p_modules[p_arg].installer.getReverseDeps():
            execute(p_modules, c_dep, p_method, p_force)

    if p_method == "install":
        p_modules[p_arg].installer.install(p_force)
    elif p_method == "uninstall":
        p_modules[p_arg].installer.uninstall(p_force)

#---------------------------------------------------------------------------#

def main():
    try:
        config.init_config(setup.GLOBAL_CONFIG,
                           setup.validation_handler,
                           setup.cmdline_init_handler,
                           setup.cmdline_process_handler)
    except exceptions.ConfigException, l_error:
        print str(l_error)
        sys.exit(1)

    l_targets = []
    l_modules = {}

    l_targets.append(config.get("general", "modules"))
    for c_target in l_targets:
        if not moduleExists(c_target):
            print "error : target <%s> not found" % c_target
            sys.exit(1)

    for c_target in l_targets:
        l_module = moduleImport(c_target)
        l_module.installer = l_module.Installer()
        l_modules[l_module.m_name] = l_module

    l_res = {}
    while len(l_modules):
        l_name, l_module = l_modules.popitem()
        print "... check module dependency %s" % l_name
        for c_dep in l_module.installer.m_dependencies:
            if not moduleExists(c_dep):
                print "error : requiered dependency %s not found" % c_dep
                sys.exit(1)
            if (not c_dep in l_res) and not (c_dep in l_modules):
                print "... loading dependency %s" % c_dep
                l_m = moduleImport(c_dep)
                l_m.installer = m.Installer()
                l_modules[c_dep] = l_m
        for c_dep in l_module.installer.getReverseDeps():
            if not moduleExists(c_dep):
                print "error : requiered reverse dependency %s not found" % c_dep
                sys.exit(1)
            if (not c_dep in l_res) and not (c_dep in l_modules):
                print "... loading dependency %s" % c_dep
                l_m = moduleImport(c_dep)
                l_m.installer = l_m.Installer()
                l_modules[c_dep] = l_m
        l_res[l_name] = l_module
    l_modules = l_res
    for c_m in l_modules.keys():
        print "... checking circular references for %s" % c_m
        checkCircularReference(c_m, l_modules, l_modules[c_m], [])

    for c_m in l_modules:
        l_modules[c_m].installer.initialize()

    l_doForce = config.get("general", "force")
    for c_target in l_targets:
        if config.get("__internal", "action") == "install" :
            execute(l_modules, c_target, "install", l_doForce)
        elif config.get("__internal", "action") == "uninstall" :
            execute(l_modules, c_target, "uninstall", l_doForce)
        elif config.get("__internal", "action") == "reinstall" :
            execute(l_modules, c_target, "uninstall", l_doForce)
            execute(l_modules, c_target, "install", l_doForce)

    for c_m in l_modules:
        l_modules[c_m].installer.finilize()

#---------------------------------------------------------------------------#

if __name__ == "__main__":
    main()

