# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.instrset.base import BaseInstruction
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet

# ---------------------------------------------------------------------------- #

class Ll(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_arg3, p_arg4, p_arg5, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Ll, 7, 0b1111, 0b0011, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2
        self.m_arg3 = p_arg3
        self.m_arg4 = p_arg4
        self.m_arg5 = p_arg5

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_value = (self.m_arg5 << 12) + (self.m_arg4 << 8) + (self.m_arg3 << 4) + self.m_arg2
        l_rx.setValue(l_value)
        p_data.append({
            "action" : "register",
            "name"   : l_rx.getName(),
            "value"  : l_rx.getValue()
        })



    def __str__(self):
        l_value = (self.m_arg5 << 12) + (self.m_arg4 << 8) + (self.m_arg3 << 4) + self.m_arg2
        return  "ll r%s, %s%s%s%s(%d) : %s" % (self.m_arg1,
                                               Quartet(self.m_arg2),
                                               Quartet(self.m_arg3),
                                               Quartet(self.m_arg4),
                                               Quartet(self.m_arg5),
                                               l_value,
                                               BaseInstruction.__str__(self))

    def evaluate(self, p_pit):
        l_n = self.m_arg2()
        if (l_n > 65535) or (l_n < -32768):
            p_pit.overflow(self, l_n, "16bit")
        self.m_arg2 = (l_n & 0b0000000000001111);
        self.m_arg3 = (l_n & 0b0000000011110000) >> 4;
        self.m_arg4 = (l_n & 0b0000111100000000) >> 8;
        self.m_arg5 = (l_n & 0b1111000000000000) >> 12;

    def serializeArgs(self):
        return [ Quartet(self.m_arg1),
                 Quartet(self.m_arg2),
                 Quartet(self.m_arg3),
                 Quartet(self.m_arg4),
                 Quartet(self.m_arg5) ]
