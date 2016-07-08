# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Str(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Str, 3, 0b1110, None, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2
        self.m_nbWrite = 0

    def __str__(self):
        return  "str [r%s(%d)], r%s(%d) : %s" % (self.m_arg1,
                                                 self.m_ship.getRegister(self.m_arg1).getValue(),
                                                 self.m_arg2,
                                                 self.m_ship.getRegister(self.m_arg2).getValue(),
                                                 BaseInstruction.__str__(self))

    def isFinished(self):
        return self.m_nbWrite == 4

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_ry = self.m_ship.getRegister(self.m_arg2)
        l_offset = l_rx.getValue() + self.m_nbWrite
        l_chunk = self.m_circuit.getChunkFromShip(self.m_ship, l_offset)
        l_value = l_ry.getValue();
        if self.m_nbWrite == 0:
            l_dataPart = (l_value & 0b0000000000001111)
        elif self.m_nbWrite == 1:
            l_dataPart = (l_value & 0b0000000011110000) >> 4
        elif self.m_nbWrite == 2:
            l_dataPart = (l_value & 0b0000111100000000) >> 8
        elif self.m_nbWrite == 3:
            l_dataPart = (l_value & 0b1111000000000000) >> 12

        l_chunk.addVote(Quartet(l_dataPart))
        self.m_circuit.m_writes.append(l_chunk.getID())
        self.m_nbWrite += 1
        p_data.append({ "action" : "write", "value" : l_dataPart, "chunk" : l_chunk.getID() })

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2) ]
