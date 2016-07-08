#!/usr/bin/python
# -*- coding: utf-8
#------------------------------------------------------------------#

import Queue
from pyscript.logger import get_logger

#------------------------------------------------------------------#

class LoggingObject(object):
    ms_modules  = []
    ms_handlers = {}
    ms_types    = [ "(debug)", "(info)", "(warn)", "(error)", "(except)"]
    ms_msgSize  = 8

    def __init__(self, p_moduleName, p_logHandlers=None):
        LoggingObject.ms_modules.append(p_moduleName)
        self.m_logHandlers = p_logHandlers
        self.m_logs        = []
        self.m_name        = p_moduleName
        self.m_labelSize   = 0

    def registerHandler(self, p_handlerName, p_handlerLabel):
        LoggingObject.ms_handlers[p_handlerName] = p_handlerLabel

    def getLogs(self):
        return self.m_logs

    def doLog(self, p_func, p_typeIdx, p_handlerName, p_message, *p_args):
        if (self.m_logHandlers != None) and (not p_handlerName in self.m_logHandlers):
            return
        p_message = p_message % p_args
        l_labelSize  = max([ len(x) for x in LoggingObject.ms_handlers.values() ])
        l_moduleSize = max([ len(x) for x in LoggingObject.ms_modules ]) + 2
        l_type = "%%%ds" % l_moduleSize
        l_moduleStr = l_type % ("[%s]" % self.m_name)
        l_type = "%%-%ds" % LoggingObject.ms_msgSize
        l_typeStr = l_type % LoggingObject.ms_types[p_typeIdx]
        l_type = "%%-%ds" % l_labelSize
        l_label   = LoggingObject.ms_handlers[p_handlerName]
        l_labelStr = l_type % l_label
        l_message = "%s -> %s %s" % (l_moduleStr,
                                     l_labelStr,
                                     p_message)
        self.m_logs.append(l_message)
        l_message = "%s %s" % (l_typeStr, l_message)
        p_func(l_message)
        return l_message

    def debug(self, p_handlerName, p_message, *p_args, **p_kwds):
        return self.doLog(get_logger().debug, 0, p_handlerName, p_message, *p_args)

    def info(self, p_handlerName, p_message, *p_args, **p_kwds):
        return self.doLog(get_logger().info, 1, p_handlerName, p_message, *p_args)

    def warning(self, p_handlerName, p_message, *p_args, **p_kwds):
        return self.doLog(get_logger().warning, 2, p_handlerName, p_message, *p_args)

    def error(self, p_handlerName, p_message, *p_args, **p_kwds):
        return self.doLog(get_logger().error, 3, p_handlerName, p_message, *p_args)

    def exception(self, p_handlerName, p_message, *p_args, **p_kwds):
        return self.doLog(get_logger().exception, 4, p_handlerName, p_message, *p_args)
