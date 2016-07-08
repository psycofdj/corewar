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
        "config-file"     : "corewar.cfg",
        "league"          : "race",
        "result"          : "best",
        "tmp-dir"         : "./run",
        "dump"            : "no"
        },

    "log" :
        {
        "file"            : "./run/log/corewar.log",
        "level"           : "30",
        "web-level"       : "40",
        "backup-number"   : "3",
        "max-size"        : "10",
        },

    "web" :
        {
        "host"           : "0.0.0.0",
        "port"           : "8080",
        "threads"        : "10",
        "daemonize"      : "yes",
        "pid-file"       : "./run/corewar.pid",
        "session-path"   : "./run/session/",
        "action"         : ""
        },


    "mysql" :
        {
        "username" : "corewar",
        "password" : "corewar",
        "host" : "corewar",
        "port" : "3306",
        "database" : "corewar"
        },

    "mail" :
        {
        "host" : "localhost",
        "port" : "25",
        "from" : "noreply@localhost"
        },

    "__internal" :
        {
        "ships"          : "",
        "compile"        : "False"
        },
    }

#------------------------------------------------------------------#

def validation_handler():
    config.check_file("log", "file", p_write=True)
    config.check_int("log", "level", 10, 50)
    config.check_int("log", "web-level", 10, 50)
    config.check_int("log", "backup-number", 1)
    config.check_float("log", "max-size", 0.0001)
    config.check_enum("general", "league", ["race", "fight"])
    config.check_enum("general", "result", ["best", "bestofuser", "all"])
    config.check_bool("general", "dump");
    config.check_dir("general", "tmp-dir", p_write=True)
    config.check_int("mysql", "port", p_minValue=1024, p_maxValue=65635)
    config.check_host("mysql", "host")
    config.check_int("web", "port", 1024, 65535)
    config.check_int("web", "threads", 1)
    config.check_enum("web", "action", ["", "start", "stop", "restart"])
    config.check_bool("web", "daemonize")
    config.check_file("web", "pid-file", p_write=True)
    config.check_host("web", "host")
    config.check_dir("web", "session-path", p_write=True)
    config.check_host("mail", "host")
    config.check_int("mail", "port", 1, 65536)
    config.check_mail("mail", "from")
    config.check_bool("__internal", "compile")

#------------------------------------------------------------------#

def cmdline_init_handler():
    l_usageFormat = "usage: %prog [options] (--start | --stop | --restart)"

    l_parser = generate_parser(l_usageFormat)

    l_group = create_group(l_parser, "General settings")
    l_group.add_option("--config-file",
                       action="store",
                       metavar="FILE",
                       dest="general_config_file",
                       help="use FILE as configuration file [default:%s]" % config.get('general', 'config-file'),
                       default=None)
    l_group.add_option("--league",
                       action="store",
                       metavar="TYPE",
                       dest="general_league",
                       help="set TYPE of league. 'fight' or 'race' [default:%s]" % config.get('general', 'league'),
                       default=None)
    l_group.add_option("--dump",
                       action="store",
                       metavar="BOOL",
                       dest="general_dump",
                       help="dump race internal data [default:%s]" % config.get('general', 'dump'),
                       default=None)
    l_group.add_option("--result",
                       action="store",
                       metavar="TYPE",
                       dest="general_result",
                       help="""use TYPE as filter of results display [default:%s]\n
                       * 'best' gives only the best ship\n
                       * 'bestofuser' give best ship for each player\n
                       * 'all' give all ships including forks."""  % config.get('general', 'result'),
                       default=None)
    l_group.add_option("-c", "--check-compile",
                       action="store_const",
                       const="True",
                       dest="internal_compile",
                       help="dot not run, only try to compile ships",
                       default=None)
    l_group.add_option("--tmp-dir",
                       action="store",
                       metavar="DIR",
                       dest="general_tmp_dir",
                       help="store temporary files to DIR. [default:%s]" % config.get('general', 'tmp-dir'),
                       default=None)
    register_group(l_group, l_parser)

    l_group = create_group(l_parser, "Logging options")
    l_group.add_option("--log-file",
                       action="store",
                       metavar="FILE",
                       dest="log_file",
                       help="logging output file. "\
                           "[default:%s]" % config.get('log', 'file'),
                       default=None)
    l_group.add_option("--log-level",
                       action="store",
                       type="int",
                       metavar="INT",
                       dest="log_level",
                       help="""set verbose level to INT [default:%s]\n
                       * 10 debug\n
                       * 20 info\n
                       * 30 warning\n
                       * 40 error\n
                       * 50 critical""" % config.get('log', 'level'),
                       default=None)
    l_group.add_option("--log-web-level",
                       action="store",
                       metavar="INT",
                       dest="log_web_level",
                       help="web server log level [default:%s]" % config.get('log', 'web-level'),
                       default=None)
    l_group.add_option("--log-backup-number",
                       action="store",
                       type="int",
                       metavar="INT",
                       dest="log_backup_number",
                       help="set number of log file backups to INT "\
                           "[default:%s]" % config.get('log', 'backup-number'),
                       default=None)
    l_group.add_option("--log-max-size",
                       action="store",
                       type="int",
                       metavar="INT",
                       dest="log_max_size",
                       help="maximum log file size in MBytes. "\
                           "[default:%s]" % config.get('log', 'max-size'),
                       default=None)
    register_group(l_group, l_parser)

    l_group = create_group(l_parser, "Mysql settings")
    l_group.add_option("--mysql-host",
                       action="store",
                       dest="mysql_host",
                       metavar="HOST",
                       help="mysql database HOST. " \
                           "[default : %s]" % config.get('mysql', 'host'),
                       default=None)
    l_group.add_option("--mysql-port",
                       action="store",
                       dest="mysql_port",
                       type="int",
                       metavar="PORT",
                       help="msyql database PORT. " \
                           "[default : %s]" % config.get('mysql', 'port'),
                       default=None)
    l_group.add_option("--mysql-database",
                       action="store",
                       dest="mysql_database",
                       metavar="NAME",
                       help="mysql database NAME. " \
                           "[default : %s]" % config.get('mysql', 'database'),
                       default=None)
    l_group.add_option("--mysql-username",
                       action="store",
                       dest="mysql_username",
                       metavar="NAME",
                       help="user NAME to connect to mysql database. " \
                           "[default : %s]" % config.get('mysql', 'username'),
                       default=None)
    l_group.add_option("--mysql-password",
                       action="store",
                       dest="mysql_password",
                       metavar="PASSWD",
                       help="password to connect to mysql database. " \
                           "[default : *******]",
                       default=None)
    register_group(l_group, l_parser)


    l_group = create_group(l_parser, "Mail settings")
    l_group.add_option("--mail-host",
                       action="store",
                       dest="mail_host",
                       metavar="HOST",
                       help="send mail to smtp HOST. " \
                           "[default : %s]" % config.get('mail', 'host'),
                       default=None)
    l_group.add_option("--mail-port",
                       action="store",
                       dest="mail_port",
                       type="int",
                       metavar="PORT",
                       help="send mail to smtp PORT. " \
                           "[default : %s]" % config.get('mail', 'port'),
                       default=None)
    l_group.add_option("--mail-from",
                       action="store",
                       dest="mail_from",
                       metavar="NAME",
                       help="Send mail Using NAME as sender." \
                           "[default : %s]" % config.get('mail', 'from'),
                       default=None)
    register_group(l_group, l_parser)

    l_group = create_group(l_parser, "Web options")
    l_group.add_option("--web-host",
                       action="store",
                       metavar="HOST",
                       dest="web_host",
                       help="use HOST for web server interface [default:%s]" % config.get('web', 'host'),
                       default=None)
    l_group.add_option("--web-port",
                       action="store",
                       metavar="PORT",
                       dest="web_port",
                       help="use PORT for web server [default:%s]" % config.get('web', 'port'),
                       default=None)
    l_group.add_option("--web-threads",
                       action="store",
                       metavar="PORT",
                       dest="web_threads",
                       help="web server number of threads [default:%s]" % config.get('web', 'threads'),
                       default=None)
    l_group.add_option("--web-daemonize",
                       action="store",
                       metavar="BOOL",
                       dest="web_daemonize",
                       help="should webserver stats as a daemon ? choose 'yes' or 'no' [default:%s]" % config.get('web', 'daemonize'),
                       default=None)
    l_group.add_option("--web-pid-file",
                       action="store",
                       metavar="FILE",
                       dest="web_pid_file",
                       help="store pid to FILE when daemonizing web server [default:%s]" % config.get('web', 'pid-file'),
                       default=None)
    l_group.add_option("--web-session-path",
                       action="store",
                       metavar="FILE",
                       dest="web_session_path",
                       help="store sessions data to DIR [default:%s]" % config.get('web', 'session-path'),
                       default=None)
    l_group.add_option("--web-start",
                       action="store_const",
                       const="start",
                       dest="web_action",
                       help="start web server",
                       default=None)
    l_group.add_option("--web-stop",
                       action="store_const",
                       const="stop",
                       dest="web_action",
                       help="stop web server",
                       default=None)
    l_group.add_option("--web-restart",
                       action="store_const",
                       const="restart",
                       dest="web_action",
                       help="restart web server",
                       default=None)
    register_group(l_group, l_parser)

    return l_parser

#------------------------------------------------------------------#

def affect(p_sectionName, p_optionName, p_value):
    if p_value != None:
        config.set(p_sectionName, p_optionName, p_value)

def cmdline_process_handler(p_cmdlineOptions, p_remainingArgs):
    affect("general",        "config-file",   p_cmdlineOptions.general_config_file)
    affect("general",        "league",        p_cmdlineOptions.general_league)
    affect("general",        "result",        p_cmdlineOptions.general_result)
    affect("general",        "tmp-dir",       p_cmdlineOptions.general_tmp_dir)
    affect("general",        "dump",          p_cmdlineOptions.general_dump)
    affect("log",            "file",          p_cmdlineOptions.log_file)
    affect("log",            "level",         p_cmdlineOptions.log_level)
    affect("log",            "backup-number", p_cmdlineOptions.log_backup_number)
    affect("log",            "max-size",      p_cmdlineOptions.log_max_size)
    affect("log",            "web-level",     p_cmdlineOptions.log_web_level)
    affect("mysql",          "host",          p_cmdlineOptions.mysql_host)
    affect("mysql",          "port",          p_cmdlineOptions.mysql_port)
    affect("mysql",          "database",      p_cmdlineOptions.mysql_database)
    affect("mysql",          "username",      p_cmdlineOptions.mysql_username)
    affect("mysql",          "password",      p_cmdlineOptions.mysql_password)
    affect("mail",           "host",          p_cmdlineOptions.mail_host)
    affect("mail",           "port",          p_cmdlineOptions.mail_port)
    affect("mail",           "from",          p_cmdlineOptions.mail_from)
    affect("web",            "host",          p_cmdlineOptions.web_host)
    affect("web",            "port",          p_cmdlineOptions.web_port)
    affect("web",            "threads",       p_cmdlineOptions.web_threads)
    affect("web",            "pid-file",      p_cmdlineOptions.web_pid_file)
    affect("web",            "session-path",  p_cmdlineOptions.web_session_path)
    affect("web",            "daemonize",     p_cmdlineOptions.web_daemonize)
    affect("web",            "action",        p_cmdlineOptions.web_action)
    affect("__internal",     "compile",       p_cmdlineOptions.internal_compile)
    config.set("__internal", "ships",         p_remainingArgs)

#------------------------------------------------------------------#

