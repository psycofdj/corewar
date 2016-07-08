# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Ldb(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_arg3, p_arg4, p_arg5, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Ldb, 7, 0b1111, 0b0000, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2
        self.m_arg3 = p_arg3
        self.m_arg4 = p_arg4
        self.m_arg5 = p_arg5
        self.m_readData = []

    def isFinished(self):
        l_m = (self.m_arg5 << 4) + self.m_arg4
        return len(self.m_readData) == l_m

    def __str__(self):
        l_n = (self.m_arg3 << 4) + self.m_arg2
        l_m = (self.m_arg5 << 4) + self.m_arg4
        return  "ldb r%s, %s%s(%d), %s%s(%d) : %s" % (self.m_arg1,
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
        l_m        = (self.m_arg5 << 4) + self.m_arg4
        l_offset = l_rx.getValue() + len(self.m_readData)
        l_chunk = self.m_circuit.getChunkFromShip(self.m_ship, l_offset)
        l_dataQuart = l_chunk.getData()
        self.m_readData.append(l_dataQuart)
        if len(self.m_readData) == l_m:
            l_destOffset = l_n
            for c_quart in self.m_readData:
                self.m_ship.writeBuffer(c_quart, l_destOffset)
                p_data.append({ "action" : "write_buffer", "value" : c_quart.getValue(), "offest" : l_destOffset })
                l_destOffset += 1

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
