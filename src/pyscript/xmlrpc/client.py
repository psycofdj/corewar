# -*- coding: utf-8
import xmlrpclib
import socket
from pyscript import config
from pyscript.logger.object import LoggingObject


def connected(p_func):
    def wrapper(*args, **kwds):
        self = args[0]
        if not self.m_isConnected:
            raise Exception, "not connected to remote server"
        return p_func(*args, **kwds)
    return wrapper


class Namespace:
    def __init__(self, p_name):
        self.__m_methods = {}
        self.__m_childNameSpaces = {}
        self.__m_name = p_name

    def addMethod(self, p_name, p_func):
        if not p_name.count("."):
            self.__m_methods[p_name] = p_func
        else:
            l_subNamespace = p_name[:p_name.find(".")]
            l_methodName = p_name[p_name.find(".")+1:]
            if not l_subNamespace in self.__m_childNameSpaces:
                l_namespace = Namespace(l_subNamespace)
                self.__m_childNameSpaces[l_subNamespace] = l_namespace
            self.__m_childNameSpaces[l_subNamespace].addMethod(l_methodName, p_func)

    def listMethods(self):
        l_methods = []
        for l_childNamespace in self.__m_childNameSpaces:
            for l_childMethod in self.__m_childNameSpaces[l_childNamespace].listMethods():
                l_methods.append("%s.%s" % (l_childNamespace, l_childMethod))
        for l_method in self.__m_methods:
            l_methods.append(l_method)
        return l_methods

    def listChildNameSpace(self):
        return self.__m_childNameSpaces.keys()

    def __getattr__(self, p_name):
        if p_name in self.__m_methods:
            return self.__m_methods[p_name]
        elif p_name in self.__m_childNameSpaces:
            return self.__m_childNameSpaces[p_name]
        else:
            raise AttributeError, "no attribute '%s' in namspace '%s'" % (p_name, self.__m_name)

class XmlrpcClient:
    def __init__(self, p_host, p_port):
        self.m_host = p_host
        self.m_port = p_port
        self.m_uri = "http://%s:%d" % (self.m_host, self.m_port)
        self.m_client = xmlrpclib.ServerProxy(self.m_uri, allow_none=True)
        self.m_isConnected = False
        self.m_rootNameSpace = Namespace("root")

    def connect(self):
        try:
            l_methodNameList = self.__listMethods()
        except:
            raise Exception, "Could not reach server %s" % self.m_uri
        l_methods = []
        for l_methodName in l_methodNameList:
            l_object = self.m_client
            l_name = l_methodName
            while not l_name.count("."):
                l_attrName = l_name[:l_name.find(".")]
                l_name = l_name[l_name.find(".")+1:]
                l_object = getattr(l_object, l_attrName)
            l_methods.append({"name" : l_methodName, "func" : getattr(l_object, l_name)})
        for l_method in l_methods:
            self.m_rootNameSpace.addMethod(l_method["name"], l_method["func"])
        self.m_isConnected = True

    @connected
    def listMethods(self):
        return self.m_rootNameSpace.listMethods()

    @connected
    def __getattr__(self, p_name):
            return getattr(self.m_rootNameSpace, p_name)

    def __listMethods(self):
        try:
            return self.m_client.system.listMethods()
        except socket.error, l_exception:
            raise Exception, "caught error while querying xmlrpc server : %s" % str(l_exception)

