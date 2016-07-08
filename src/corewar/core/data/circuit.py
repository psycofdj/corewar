# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data.chunk import Chunk
from pyscript.exceptions     import BaseException

# ---------------------------------------------------------------------------- #

class Circuit:
    def __init__(self):
        self.m_chunks = []
        self.m_size   = 0
        self.m_writes = []

    def getSize(self):
        return len(self.m_chunks)
    def getChunks(self):
        return self.m_chunks

    def generateChunks(self, p_circuitSize):
        self.m_size   = p_circuitSize
        self.m_chunks = [ Chunk(c_id) for c_id in range(p_circuitSize) ]

    def getChunkByID(self, p_chunkID):
        try:
            return self.m_chunks[p_chunkID]
        except IndexError:
            l_message = "attempt to get chunk '%d' on track size '%d'"
            l_message = l_message % (p_chunkID, self.m_size)
            raise BaseException(l_message, "circuit")

    def getChunkByPos(self, p_chunkPos):
        l_chunkID = p_chunkPos % self.getSize()
        return self.getChunkByID(l_chunkID)

    def getReachableOffset(self, p_ship, p_offset):
        l_limit = p_ship.getMode().Sight
        while not (p_offset < -l_limit) and (p_offset >= l_limit):
            if p_offset > 0:
                p_offset -= 2 * l_limit
            else:
                p_offset += 2 * l_limit
        return p_offset

    def getChunkFromShip(self, p_ship, p_offset = 0):
        l_reachableOffset = self.getReachableOffset(p_ship, p_offset)
        l_chunk           = self.getChunkByPos(p_ship.getPC() + l_reachableOffset)
        return l_chunk

    def moveShip(self, p_ship, p_offset):
        l_reachableOffset = self.getReachableOffset(p_ship, p_offset)
        l_chunk = self.getChunkByPos(p_ship.getPC() + l_reachableOffset)
        p_ship.movePC(l_reachableOffset)
        return l_chunk

    def placeShip(self, p_ship, p_startID):
        l_offset = 0
        for c_quartet in p_ship.getInitialCode():
            self.getChunkByID(p_startID + l_offset).getData().copy(c_quartet)
            l_offset += 1


