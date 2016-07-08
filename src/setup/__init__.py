#!/usr/bin/python
# -*- coding: utf-8
#------------------------------------------------------------------#

import os
import re
from pyscript import config
from pyscript.config.cmdline import create_group, register_group, generate_parser

#------------------------------------------------------------------#

GLOBAL_CONFIG = {
    "general" :
        {
        "force"       : "false",
        "keep"        : "false",
        "modules"     : "",
        },
    "mysql" :
        {
        "username"    : None,
        "password"    : None,
        },
    "__internal" :
        {
        "action"      : ""
        },
    }

#------------------------------------------------------------------#

def validation_handler():
    config.check_bool("general", "force")
    config.check_bool("general", "keep")
    config.check_enum("__internal", "action", ["install", "uninstall", "reinstall"])
    config.check_enum("general", "modules",   ["corewar"])

#------------------------------------------------------------------#

def cmdline_init_handler():
    l_usageFormat = "usage: %prog [options] (--install | --uninstall | --reinstall) --modules=corewar"

    l_parser = generate_parser(l_usageFormat)

    l_group = create_group(l_parser, "General settings")
    l_group.add_option("--force",
                       action="store_const",
                       const="true",
                       dest="general_force",
                       help="Force operations when already installed. " \
                           "[default %s]" % config.get('general', 'force'),
                       default="false")
    l_group.add_option("--keep",
                       action="store_const",
                       const="true",
                       dest="general_keep",
                       help="Keep data when installing/uninstalling modules. " \
                           "[default %s]" % config.get('general', 'keep'),
                       default="false")
    l_group.add_option("--modules",
                       action="store",
                       dest="general_modules",
                       metavar="LIST",
                       help="list of modules to process. " \
                           "[default %s]" % config.get('general', 'modules'),
                       default=None)
    register_group(l_group, l_parser)
    l_group = create_group(l_parser, "Mysql settings")
    l_group.add_option("--mysql-username",
                       action="store",
                       dest="mysql_username",
                       metavar="NAME",
                       help="Mysql admin login " \
                           "[default : %s]" % config.get('mysql', 'username'),
                       default=None)
    l_group.add_option("--mysql-password",
                       action="store",
                       dest="mysql_password",
                       metavar="PASSWD",
                       help="Mysql admin password",
                       default=None)
    register_group(l_group, l_parser)
    l_group = create_group(l_parser, "Command settings")
    l_group.add_option("--install",
                       action="store_const",
                       const="install",
                       dest="action",
                       help="install program",
                       default=None)
    l_group.add_option("--uninstall",
                       action="store_const",
                       const="uninstall",
                       dest="action",
                       help="uninstall program",
                       default=None)
    l_group.add_option("--reinstall",
                       action="store_const",
                       const="reinstall",
                       dest="action",
                       help="reinstall program",
                       default=None)
    register_group(l_group, l_parser)
    return l_parser

#------------------------------------------------------------------#

def affect(p_sectionName, p_optionName, p_value):
    if p_value != None:
        config.set(p_sectionName, p_optionName, p_value)

def cmdline_process_handler(p_cmdlineOptions, p_args):
    affect("general",    "force",    p_cmdlineOptions.general_force)
    affect("general",    "keep",     p_cmdlineOptions.general_keep)
    affect("general",    "modules",  p_cmdlineOptions.general_modules)
    affect("mysql",      "username", p_cmdlineOptions.mysql_username)
    affect("mysql",      "password", p_cmdlineOptions.mysql_password)
    affect("__internal", "action",   p_cmdlineOptions.action)

#------------------------------------------------------------------#

