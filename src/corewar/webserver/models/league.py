# -*- coding: utf-8
#---------------------------------------------------------------------------#

import re
from pyscript               import config
from pyscript.exceptions    import SqlExecuteException
from pyscript.sql.handler   import sqlDefaultHandler, makeSqlConfig, autocommit, autoconnect

#---------------------------------------------------------------------------#

class League(sqlDefaultHandler):
    def __init__(self):
        l_config = makeSqlConfig(config.get("mysql", "username"),
                                 config.get("mysql", "password"),
                                 config.get("mysql", "host"),
                                 config.get("mysql", "database"))
        sqlDefaultHandler.__init__(self, l_config)

    @autoconnect
    @autocommit
    def getByID(self, p_id):
        return self.selectFirst(["*"], "time_results", {"id" : int(p_id)});

    @autoconnect
    @autocommit
    def getResults(self):
        l_query = """
        SELECT
          time_results.id       as id,
          user.nickname         as nickname,
          time_results.uid      as uid,
          time_results.name     as name,
          time_results.log      as log,
          time_results.finished as finished,
          time_results.cycles   as cycles,
          time_results.date     as date
        FROM time_results
        JOIN user ON time_results.uid = user.id
        ORDER BY
           finished DESC,
           cycles   ASC,
           date     ASC
        """
        return self.execute(l_query)
