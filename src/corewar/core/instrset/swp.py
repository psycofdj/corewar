# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Swp(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Swp, 4, 0b1111, 0b0100, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2

    def __str__(self):
        return  "swp r%s(%d) r%s(%d) : %s" % (self.m_arg1,
                                              self.m_ship.getRegister(self.m_arg1).getValue(),
                                              self.m_arg2,
                                              self.m_ship.getRegister(self.m_arg2).getValue(),
                                              BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_ry = self.m_ship.getRegister(self.m_arg2)
        l_val = l_rx.getValue()
        l_rx.setValue(l_ry.getValue())
        l_ry.setValue(l_val)
        p_data.append({
            "action" : "register",
            "name"   : l_rx.getName(),
            "value"  : l_rx.getValue()
        })
        p_data.append({
            "action" : "register",
            "name"   : l_ry.getName(),
            "value"  : l_ry.getValue()
        })

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2) ]

