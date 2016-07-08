# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Rol(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Rol, 3, 0b0110, None, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2

    def __str__(self):
        return  "rol r%s(%d) %d : %s" % (self.m_arg1,
                                         self.m_ship.getRegister(self.m_arg1).getValue(),
                                         self.m_arg2,
                                         BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_n  = self.m_arg2
        l_value = l_rx.getValue()
        for c_idx in range(l_n):
            l_bit = l_value & 0b1000000000000000
            l_bit >> 15
            l_value << 1
            l_value += l_bit
        l_rx.setValue(l_value)
        self.m_ship.setS(l_rx.isNeg())
        self.m_ship.setZ(l_rx.isNull())
        p_data.append({
            "action" : "register",
            "name"   : l_rx.getName(),
            "value"  : l_rx.getValue()
        })
        p_data.append({
            "action" : "sz",
            "z"      : l_rx.isNull(),
            "s"      : l_rx.isNeg()
        })

    def evaluate(self, p_pit):
        l_n = self.m_arg2()
        if (l_n > 15) or (l_n < -8):
            p_pit.overflow(self, l_n, "4bit")
        self.m_arg2 = l_n

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2) ]
