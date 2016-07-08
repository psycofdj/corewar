# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Lc(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_arg3, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Lc, 5, 0b1111, 0b0010, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2
        self.m_arg3 = p_arg3


    def __str__(self):
        l_value = (self.m_arg3 << 4) + self.m_arg2
        return  "lc r%s %d : %s" % (self.m_arg1,
                                    l_value,
                                    BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_value = (self.m_arg3 << 4) + self.m_arg2
        if (l_value & 0b10000000) >> 7:
            l_value | -128
        l_rx.setValue(l_value)
        p_data.append({
            "action" : "register",
            "name"   : l_rx.getName(),
            "value"  : l_rx.getValue()
        })

    def evaluate(self, p_pit):
        l_n = self.m_arg2()
        if (l_n > 256) or (l_n < -128):
            p_pit.overflow(self, l_n, "8bit")
        self.m_arg2 = (l_n & 0b00001111);
        self.m_arg3 = (l_n & 0b11110000) >> 4;

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2), Quartet(self.m_arg3) ]

