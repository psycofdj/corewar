#!/usr/bin/python -OO
# -*-coding:UTF-8 -*
#---------------------------------------------------------------------------#

import MySQLdb
import re
import sys

from pyscript.tools      import types
from pyscript.exceptions import SqlExecuteException

#---------------------------------------------------------------------------#

def makeSqlConfig(p_user, p_passwd, p_host, p_db = None):
    l_rep             = {}
    l_rep['user']     = p_user
    l_rep['password'] = p_passwd
    l_rep['server']   = p_host
    l_rep['db']       = p_db
    return l_rep

#---------------------------------------------------------------------------#

def autocommit(p_func):
    def wrapped(self, *p_args, **p_kwds):
        self.startTransaction()
        l_data = p_func(self, *p_args, **p_kwds)
        self.commit()
        return l_data
    return wrapped
#---------------------------------------------------------------------------#

def autoconnect(p_func):
    def wrapped(self, *p_args, **p_kwds):
        self.connect()
        l_data = p_func(self, *p_args, **p_kwds)
        self.disconnect()
        return l_data
    return wrapped

#---------------------------------------------------------------------------#

class sqlDefaultHandler:
    def __init__(self, p_sqlConfig):
        self.m_config = p_sqlConfig
        self.m_sqlFunctions  = []
        self.m_sqlFunctions.append("NOW()")
        self.m_sqlFunctions.append("CURRENT_DATE()")
        self.m_sqlFunctions.append("NULL")
        self.m_sqlFunctions.append("SHA2")
        self.m_connection = None

    def hasDatabase(self, p_dbName):
        l_query = "SHOW databases LIKE '%s';" % p_dbName
        l_data = self.execute(l_query)
        return len(l_data) == 1

    def hasUser(self, p_userName):
        l_query = "SELECT * FROM mysql.user WHERE user='%s'" % p_userName
        l_data = self.execute(l_query)
        return len(l_data) == 1

    def hasTable(self, p_tableName, p_dbName = None):
        if p_dbName != None:
            l_query = "SHOW tables FROM %s LIKE '%s';" % (p_dbName, p_tableName)
        else:
            l_query = "SHOW tables LIKE '%s';" % p_tableName
        l_data = self.execute(l_query)
        return len(l_data) == 1

    def testConnexion(self):
        try:
            if self.m_config['db'] != None:
                l_connection = MySQLdb.connect(host   = self.m_config['server'],
                                               user   = self.m_config['user'],
                                               passwd = self.m_config['password'],
                                               db     = self.m_config['db'])
            else:
                l_connection = MySQLdb.connect(host   = self.m_config['server'],
                                               user   = self.m_config['user'],
                                               passwd = self.m_config['password'])
            l_cursor = connection.cursor()
            l_cursor.execute("SELECT VERSION()")
            l_cursor.close()
            l_connection.close()
        except MySQLdb.OperationalError:
            return False
        return True

    def connect(self, p_host = None, p_user = None, p_passwd = None, p_db = None):
        if p_host == None:
            p_host = self.m_config['server']

        if p_user == None:
            p_user = self.m_config['user']

        if p_passwd == None:
            p_passwd = self.m_config['password']

        if p_db == None:
            p_db = self.m_config['db']

        if p_db != None:
            self.m_connection = MySQLdb.connect(host=p_host, user=p_user, passwd=p_passwd, db=p_db, use_unicode=True, charset="utf8")
        else:
            self.m_connection = MySQLdb.connect(host=p_host, user=p_user, passwd=p_passwd, use_unicode=True, charset="utf8")

    def disconnect(self):
        self.m_connection.close()

    def reconnect(self):
        self.disconnect()
        self.connect()

    def use(self, p_db):
        self.execute("USE `%s`;" % p_db)

    def execute(self, p_query):
        try:
            l_cursor = self.m_connection.cursor()
            l_cursor.execute(p_query)
            l_results = l_cursor.fetchall()
            l_descr = l_cursor.description
            l_data = []
            for c_res in l_results:
                l_row = {}
                for c_i in range(len(l_descr)):
                    l_value = c_res[c_i]
                    l_row[l_descr[c_i][0]] = l_value
                l_data.append(l_row)
            l_cursor.close()
            return l_data
        except MySQLdb.MySQLError, l_error:
            raise SqlExecuteException(p_query, l_error)

    def startTransaction(self):
        self.execute("START TRANSACTION;")

    def commit(self):
        self.execute("COMMIT;")

    def quoteItem(self, p_val):
        if types.is_int(p_val):
            l_item = str(p_val)
        elif types.is_bool(p_val):
            if p_val:
                l_item = 1
            else:
                l_item = 0
        else:
            l_found = False
            for c_fun in self.m_sqlFunctions:
                if p_val.startswith(c_fun):
                    l_found = True
            if not l_found:
                p_val = re.sub('\'', '\\\'', p_val)
                l_item = "'%s'" % p_val
            else:
                l_item = "%s" % p_val
        return l_item

    def lockTable(self, p_table, p_mode = "write"):
        if p_mode == "write":
            p_mode = "WRITE"
        else:
            p_mode = "READ"
        l_query = "LOCK TABLES %s %s" % (p_table, p_mode)
        self.execute(l_query)

    def unlockTables(self):
        l_query = "UNLOCK TABLES"
        self.execute(p_query)

    def __buildSelect(self, p_cols, p_table, p_cond, p_order):
        p_cols  = types.to_array(p_cols)
        l_query = "SELECT %s FROM %s" % (", ".join(p_cols), p_table)
        if p_cond:
            p_cond = ["%s=%s" % (x, self.quoteItem(y)) for x,y in p_cond.items()]
            p_cond = " AND ".join(p_cond)
            l_query += " WHERE %s" % p_cond
        if p_order:
            p_order = ["%s %s" % (x,y) for x,y in p_order.items()]
            p_order = ", ".join(p_order)
            l_query += " ORDER %s" % p_order
        return l_query

    def select(self, p_cols, p_table, p_cond = None, p_order = None):
        l_query = self.__buildSelect(p_cols, p_table, p_cond, p_order)
        return self.execute(l_query)

    def selectFirst(self, p_cols, p_table, p_cond = None, p_order = None):
        l_query = self.__buildSelect(p_cols, p_table, p_cond, p_order)
        l_data  = self.execute(l_query)
        if len(l_data):
            return l_data[0]
        return None

    def insert(self, p_data, p_table):
        l_query = "INSERT INTO `%s` (" % p_table
        l_keys = p_data.keys()
        for c_idx in range(len(l_keys)):
            l_query += l_keys[c_idx]
            if (c_idx != len(l_keys) - 1):
                l_query += ", "
        l_query += ") VALUES("
        for c_idx in range(len(l_keys)):
            l_item = p_data[l_keys[c_idx]]
            l_query += self.quoteItem(l_item)
            if (c_idx != len(l_keys) - 1):
                l_query += ", "
        l_query += ");"
        self.execute(l_query)
        return self.getLastId()

    def update(self, p_data, p_table, p_conditions = None, p_op = "AND"):
        l_query = "UPDATE `%s` SET " % p_table
        l_keys = p_data.keys()
        for c_idx in range(len(l_keys)):
            l_item = p_data[l_keys[c_idx]]
            l_query += l_keys[c_idx] + "="
            l_query += self.quoteItem(l_item)
            if (c_idx != len(l_keys) - 1):
                l_query += ", "
        if (None != p_conditions):
            l_query += " WHERE "
            l_keys = p_conditions.keys()
            for c_idx in range(len(l_keys)):
                l_item = p_conditions[l_keys[c_idx]]
                l_query += l_keys[c_idx] + "="
                l_query += self.quoteItem(l_item)
                if (c_idx != len(l_keys) - 1):
                    l_query += " " + p_op + " "
        else:
            l_query += ";"
        self.execute(l_query)

    def getLastId(self):
        l_data = self.execute("SELECT LAST_INSERT_ID() as id;")
        return l_data[0]['id']

#---------------------------------------------------------------------------#





