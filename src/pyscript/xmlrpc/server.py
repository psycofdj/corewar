# -*- coding: utf-8
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from pyscript.tools import net
from pyscript.tools import thread
from pyscript.logger.object import LoggingObject

#------------------------------------------------------------------#

class XmlrpcServer(thread.SafeThread, SimpleXMLRPCServer):
    def  __init__(self, p_host, p_port):
        self.m_port = p_port
        self.m_host = self.getHostname(p_host)
        self.m_address = (self.m_host, self.m_port)
        self.allow_reuse_address = True
        SimpleXMLRPCServer.__init__(self, self.m_address, logRequests=False)
        thread.SafeThread.__init__(self, 0, "XmlRPC server")
        self.register_introspection_functions()

    def getHostname(self, p_defaultHostname):
        l_host = p_defaultHostname
        if l_host == "auto":
            l_host = net.get_hostname()[2][0];
        return l_host

    def work(self):
        self.handle_request()
        if self.m_terminated == True:
            self.server_close()

    def stop(self, p_sendPing = True):
        self.info("Stopping XmlRPC server...")
        self.m_terminated = True
        if p_sendPing:
            self.ping()

    def ping(self):
        self.debug("sending ping request to self ... : %s:%d" % self.m_address)
        l_client = xmlrpclib.ServerProxy("http://%s:%d" % self.m_address)
        l_client.system.listMethods()

#------------------------------------------------------------------#

__instance = None
def getInstance(p_host, p_port):
    global __instance
    if __instance == None:
        __instance = XmlrpcServer(p_host, p_port)
    return __instance

#------------------------------------------------------------------#
