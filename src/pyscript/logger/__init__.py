#!/usr/bin/python
# -*- coding: utf-8
#------------------------------------------------------------------#

import logging
import sys
from logging.handlers import *

from pyscript import config

#------------------------------------------------------------------#

def init_logging(p_msgFmt = None, p_dateFmt = None):
    l_stdoutHandler = logging.StreamHandler(sys.stdout)
    l_fileHandler = RotatingFileHandler(config.get("log", "file"),
                                        maxBytes = config.get("log", "max-size") * 1024 * 1024,
                                        backupCount = config.get("log", "backup-number"))

    if p_msgFmt is None:
        p_msgFmt = "%(asctime)s -> %(message)s"
    if p_dateFmt is None:
        p_dateFmt = "%a %d %b %Y at %H-%M"


    l_format = logging.Formatter(p_msgFmt, p_dateFmt)
    l_fileHandler.setFormatter(l_format)
    l_stdoutHandler.setFormatter(l_format)
    logging.getLogger().setLevel(config.get("log", "level"))
    logging.getLogger().addHandler(l_fileHandler)
    logging.getLogger().addHandler(l_stdoutHandler)

def get_logger():
    return logging.getLogger()
