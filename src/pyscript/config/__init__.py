# -*- coding: utf-8
#------------------------------------------------------------------#

import os
import re
import socket
import copy
from stat import *
from pyscript.exceptions import *

#------------------------------------------------------------------#

def set(p_sectionName, p_optionName, p_value):
    from pyscript.config import CONFIG as g_conf
    g_conf[p_sectionName][p_optionName] = p_value

def get(p_sectionName, p_optionName):
    from pyscript.config import CONFIG as g_conf
    if (not p_sectionName in g_conf) or (not p_optionName in g_conf[p_sectionName]):
        raise ConfigValueException(p_sectionName, p_optionName, "no such parameter in config")
    return g_conf[p_sectionName][p_optionName]

#------------------------------------------------------------------#

def init_config(p_globalConfigVariable,
                p_config_validation_handler,
                p_cmdline_init_handler = None,
                p_cmdline_process_handler = None,
                p_fileconfig_init_handler = None,
                p_fileconfig_process_handler = None):
    """
    1. Parse des arguments en ligne de commande
    2. Extraction d'une eventuelle option de fichier de configuration et
    validation de l'existence du fichier
    3. Parse du fichier de configuration donne en parametre et chagement des
    donnes parsees
    4. Chargement des parametres donnes en ligne de commande
    5. Validation et typage des donnees de configuration
    """
    global CONFIG
    CONFIG = p_globalConfigVariable
    from pyscript.config import fileconfig

    #1
    l_cmdlineParser = p_cmdline_init_handler()
    l_cmdlineOptions, l_cmdlineArgs = l_cmdlineParser.parse_args()

    #2
    if hasattr(l_cmdlineOptions, "general_config_file"):
        if l_cmdlineOptions.general_config_file != None:
            set("general", "config-file", l_cmdlineOptions.general_config_file)
        check_file("general", "config-file", p_read=True)

    #3
    if hasattr(l_cmdlineOptions, "general_config_file"):
        if p_fileconfig_init_handler == None:
            p_fileconfig_init_handler = fileconfig.generate_parser
        l_fileconfigParser = p_fileconfig_init_handler(get("general", "config-file"))

    if hasattr(l_cmdlineOptions, "general_config_file"):
        if p_fileconfig_process_handler == None:
            p_fileconfig_process_handler = fileconfig.load_options
        p_fileconfig_process_handler(l_fileconfigParser)

    #4
    p_cmdline_process_handler(l_cmdlineOptions, l_cmdlineArgs)

    #5
    p_config_validation_handler()

# ------------------------------------------------------------------------- #


def init_file_config(p_globalConfigVariable,
                     p_configFile,
                     p_config_validation_handler) :

    global CONFIG
    l_oldConfig = copy.deepcopy(CONFIG)
    CONFIG = p_globalConfigVariable
    from pyscript.config import fileconfig

    l_fileconfigParser = fileconfig.generate_parser(p_configFile)
    fileconfig.load_options(l_fileconfigParser)
    p_config_validation_handler()

    def getter(p_sectionName, p_optionName):
        if ((not p_sectionName in p_globalConfigVariable) or
            (not p_optionName in p_globalConfigVariable[p_sectionName])):
            raise ConfigValueException(p_sectionName, p_optionName, "no such parameter in config")
        return p_globalConfigVariable[p_sectionName][p_optionName]

    CONFIG = l_oldConfig

    return getter

# ------------------------------------------------------------------------- #

def check_file(p_sectionName, p_optionName, p_read = False, p_write = False, p_execute = False):
    l_filePath = get(p_sectionName, p_optionName)
    l_absFilePath = os.path.abspath(l_filePath)

    if os.path.isdir(l_absFilePath):
        raise ConfigValueFileException(p_sectionName,
                                       p_optionName,
                                       l_absFilePath)
    if not os.path.isfile(l_absFilePath):
        if p_read or not check_mode(os.path.dirname(l_absFilePath), p_write=True):
            raise ConfigValueFileModeException(p_sectionName,
                                               p_optionName,
                                               l_filePath,
                                               p_read,
                                               p_write,
                                               p_execute)
    else:
        if not check_mode(l_absFilePath, p_read, p_write, p_execute):
            raise ConfigValueFileModeException(p_sectionName,
                                               p_optionName,
                                               l_filePath,
                                               p_read,
                                               p_write,
                                               p_execute)

# ------------------------------------------------------------------------- #

def check_dir(p_sectionName, p_optionName, p_read = False, p_write = False, p_execute = False):
    l_dirPath = get(p_sectionName, p_optionName)
    l_absDirPath = os.path.abspath(l_dirPath)

    if not os.path.isdir(l_absDirPath):
        raise ConfigValueDirException(p_sectionName,
                                      p_optionName,
                                      l_absDirPath)

    if not check_mode(l_absDirPath, p_read, p_write, p_execute):
        raise ConfigValueDirModeException(p_sectionName,
                                          p_optionName,
                                          l_dirPath,
                                          p_read,
                                          p_write,
                                          p_execute)

# ------------------------------------------------------------------------- #

def check_int(p_sectionName, p_optionName, p_minValue = None, p_maxValue = None):
    l_value = get(p_sectionName, p_optionName)
    try:
        l_intValue = int(l_value)
    except ValueError:
        raise ConfigValueTypeException(p_sectionName,
                                       p_optionName,
                                       l_value,
                                       ConfigTypeException.INT)
    if (p_minValue != None) and (l_intValue < p_minValue):
        raise ConfigValueLimitsException(p_sectionName,
                                         p_optionName,
                                         l_value,
                                         p_minValue,
                                         p_maxValue)
    if (p_maxValue != None) and (l_intValue > p_maxValue):
        raise ConfigValueLimitsException(p_sectionName,
                                         p_optionName,
                                         l_value,
                                         p_minValue,
                                         p_maxValue)
    set(p_sectionName, p_optionName, l_intValue)

# ------------------------------------------------------------------------- #

def check_float(p_sectionName, p_optionName, p_minValue = None, p_maxValue = None):
    l_value = get(p_sectionName, p_optionName)
    try:
        l_floatValue = float(l_value)
    except ValueError:
        raise ConfigValueTypeException(p_sectionName,
                                       p_optionName,
                                       l_value,
                                       ConfigTypeException.FLOAT)
    if (p_minValue != None) and (l_floatValue < p_minValue):
        raise ConfigValueLimitsException(p_sectionName,
                                         p_optionName,
                                         l_value,
                                         p_minValue,
                                         p_maxValue)
    if (p_maxValue != None) and (l_floatValue > p_maxValue):
        raise ConfigValueLimitsException(p_sectionName,
                                         p_optionName,
                                         l_value,
                                         p_minValue,
                                         p_maxValue)
    set(p_sectionName, p_optionName, l_floatValue)

# ------------------------------------------------------------------------- #

def check_bool(p_sectionName, p_optionName):
    l_value = get(p_sectionName, p_optionName)
    if ((l_value.lower() == 'true') or
        (l_value.lower() == 'yes') or
        (l_value.lower() == 'on')):
        set(p_sectionName, p_optionName, True)
    elif ((l_value.lower() == 'false') or
          (l_value.lower() == 'no') or
          (l_value.lower() == 'off')):
        set(p_sectionName, p_optionName, False)
    else:
        raise ConfigValueTypeException(p_sectionName,
                                       p_optionName,
                                       l_value,
                                       ConfigTypeException.BOOL)


# ------------------------------------------------------------------------- #

def check_enum(p_sectionName, p_optionName, p_authorizedValues):
    l_value = get(p_sectionName, p_optionName)
    if not l_value in p_authorizedValues:
        raise ConfigValueEnumException(p_sectionName, p_optionName, l_value, p_authorizedValues)

# ------------------------------------------------------------------------- #

def check_mode(p_path, p_read = False, p_write = False, p_execute = False):
    if not os.path.exists(p_path):
        return False
    l_uid = os.getuid()
    l_gid = os.getgid()
    l_dir_stat = os.stat(p_path)
    l_dir_uid = l_dir_stat.st_uid
    l_dir_gid = l_dir_stat.st_gid
    l_dir_mode = l_dir_stat.st_mode
    l_dir_user_mode  = l_dir_mode & 00700
    l_dir_group_mode = l_dir_mode & 00070
    l_dir_other_mode = l_dir_mode & 00007
    if l_uid == l_dir_uid:
        if p_read and not (l_dir_user_mode & 00400):
            return False
        if p_write and not (l_dir_user_mode & 00200):
            return False
        if p_execute and not (l_dir_user_mode & 00100):
            return False
    elif l_gid == l_dir_gid:
        if p_read and not (l_dir_group_mode & 00040):
            return False
        if p_write and not (l_dir_group_mode & 00020):
            return False
        if p_execute and not (l_dir_group_mode & 00010):
            return False
    else:
        if p_read and not (l_dir_other_mode & 00004):
            return False
        if p_write and not (l_dir_other_mode & 00002):
            return False
        if p_execute and not (l_dir_other_mode & 00001):
            return False
    return True
# ------------------------------------------------------------------------- #

def check_mail(p_sectionName, p_optionName):
    l_value = get(p_sectionName, p_optionName)
    l_mail_regexp = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
    if not re.match("^%s$" % l_mail_regexp, l_value):
        if not re.match("^[^<]*<%s>$" % l_mail_regexp, l_value):
            l_message = "value '%s' is not an email address" % l_value
            raise ConfigValueException(p_sectionName, p_optionName, l_message)

# ------------------------------------------------------------------------- #

def check_array(p_sectionName, p_optionName, p_checkFunc):
    l_values =  get(p_sectionName, p_optionName)
    l_values = l_values.split(",")
    for l_value in l_values:
        p_checkFunc(l_value)

# ------------------------------------------------------------------------- #

def check_host(p_sectionName, p_optionName):
    l_value = get(p_sectionName, p_optionName)
    try:
        socket.gethostbyname(l_value)
    except socket.gaierror:
        l_message = "host '%s' is not valid" % l_value
        raise ConfigValueException(p_sectionName, p_optionName, l_message)
