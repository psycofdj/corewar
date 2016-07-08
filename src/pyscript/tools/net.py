# -*- coding: utf-8
#-----------------------------------------------------------------------------#

import socket
import urllib

from pyscript.logger.object import LoggingObject

#-----------------------------------------------------------------------------#

def get_hostname():
    return socket.gethostbyaddr(socket.gethostname())

#-----------------------------------------------------------------------------#

class NetHandler(LoggingObject):
    def __init__(self):
        LoggingObject.__ini__(self, "net handler")

    @classmethod
    def encode(p_value):
        return urllib.quote_plus(p_value)

    @classmethod
    def get(p_url):
        try:
            l_document = urllib.urlopen(p_url)
        except IOError, e:
            l_error = NetException(p_url)
            self.error(str(l_error)))
            raise l_error
        return l_document

#-----------------------------------------------------------------------------#
