# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Stb(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_arg3, p_arg4, p_arg5, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Stb, 7, 0b1111, 0b0001, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2
        self.m_arg3 = p_arg3
        self.m_arg4 = p_arg4
        self.m_arg5 = p_arg5
        self.m_nbWrite  = 0

    def isFinished(self):
        l_m = (self.m_arg5 << 4) + self.m_arg4
        return self.m_nbWrite == l_m

    def __str__(self):
        l_n = (self.m_arg3 << 4) + self.m_arg2
        l_m = (self.m_arg5 << 4) + self.m_arg4
        return  "stb [r%s(%d)], %s%s(%d), %s%s(%d) : %s" % (self.m_arg1,
                                                            self.m_ship.getRegister(self.m_arg1).getValue(),
                                                            Quartet(self.m_arg2),
                                                            Quartet(self.m_arg3),
                                                            l_n,
                                                            Quartet(self.m_arg4),
                                                            Quartet(self.m_arg5),
                                                            l_m,
                                                            BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx       = self.m_ship.getRegister(self.m_arg1)
        l_n        = (self.m_arg3 << 4) + self.m_arg2
        l_offset = l_rx.getValue() + self.m_nbWrite
        l_chunk  = self.m_circuit.getChunkFromShip(self.m_ship, l_offset)
        l_quart  = self.m_ship.readBuffer(l_n + self.m_nbWrite)
        l_chunk.addVote(l_quart)
        self.m_circuit.m_writes.append(l_chunk.getID())
        p_data.append({ "action" : "write", "value" : l_quart.getValue(), "chunk" : l_chunk.getID() })
        self.m_nbWrite += 1


    def evaluate(self, p_pit):
        l_n = self.m_arg2()
        l_m = self.m_arg4()
        if (l_n > 256) or (l_n < -128):
            p_pit.overflow(self, l_n, "8bit")
        if (l_m > 256) or (l_m < -128):
            p_pit.overflow(self, l_m, "8bit")
        self.m_arg2 = (l_n & 0b00001111);
        self.m_arg3 = (l_n & 0b11110000) >> 4;
        self.m_arg4 = (l_m & 0b00001111);
        self.m_arg5 = (l_m & 0b11110000) >> 4;

    def serializeArgs(self):
        return [ Quartet(self.m_arg1),
                 Quartet(self.m_arg2),
                 Quartet(self.m_arg3),
                 Quartet(self.m_arg4),
                 Quartet(self.m_arg5) ]
