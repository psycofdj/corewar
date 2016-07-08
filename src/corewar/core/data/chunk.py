# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data.quartet import Quartet

# ---------------------------------------------------------------------------- #

class Chunk:
    def __init__(self, p_id):
        self.m_id             = p_id
        self.m_data           = Quartet()
        self.m_votes          = [] # list of Quartet
        self.m_wroteLastCycle = -1


    def copy(self, p_chunk):
        self.m_data.copy(p_chunk.m_data)
        self.m_wroteLastCycle = p_chunk.m_wroteLastCycle

    def __str__(self):
        l_str = "chunk #%d : wrote=(%s), data=%s, votes=(%s)"
        l_str = l_str % (self.m_id,
                         str(self.m_wroteLastCycle),
                         str(self.m_data),
                         ",".join([str(x) for x in self.m_votes]))
        return l_str

    def getID(self):
        return self.m_id
    def getData(self):
        return self.m_data
    def getWroteLastCycle(self):
        return self.m_wroteLastCycle
    def getVotes(self):
        return self.m_votes
    def getValue(self):
        return self.m_data.getValue()

    def setWroteLastCycle(self, p_cycle):
        self.m_wroteLastCycle = p_cycle

    def addVote(self, p_quartet):
        self.m_votes.append(p_quartet)
    def clearVotes(self):
        self.m_votes = []
