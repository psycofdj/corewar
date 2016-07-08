# -*- coding: utf-8
#------------------------------------------------------------------#

import ConfigParser
from pyscript import config
from pyscript.exceptions import FileConfigSectionException, FileConfigOptionException

#------------------------------------------------------------------#

def validate_parser(p_parser):
    """
    @brief Verifie la coherence des options qui ont ete chargees par le parser
    @param p_parser ConfigParser retourne par la fonction @see generate_parser
    @details
    Cette fonction verifie que chacun des parametres existe dans la variable
    global de configuration g_conf. On verifie egalement que ces parametres
    sont renseignes dans les bonnes sections
    """
    for l_sectionName in p_parser.sections():
        if not l_sectionName in config.CONFIG.keys():
            raise FileConfigSectionException(l_sectionName)
        for l_optionName in p_parser.options(l_sectionName):
            if not l_optionName in config.CONFIG[l_sectionName].keys():
                raise FileConfigOptionException(l_sectionName, l_optionName)


def generate_parser(p_configFile):
    """
    @brief Creer et retourne un parser de ficher de configuration
    @return parser initialise de type ConfigParser
    """
    l_configFile = p_configFile
    l_parser = ConfigParser.SafeConfigParser()
    l_parser.read(l_configFile)
    validate_parser(l_parser)
    return l_parser

def load_options(p_parser):
    """
    @brief Charge les options parsees par p_parser dans la variable global de config
    """
    for l_sectionName in p_parser.sections():
        for l_optionName in p_parser.options(l_sectionName):
            config.set(l_sectionName, l_optionName, p_parser.get(l_sectionName, l_optionName))


