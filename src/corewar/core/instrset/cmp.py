# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet, Register
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Cmp(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Cmp, 3, 0b1010, None, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2

    def __str__(self):
        return  "cmp r%s(%d) r%s(%d) : %s" % (self.m_arg1,
                                              self.m_ship.getRegister(self.m_arg1).getValue(),
                                              self.m_arg2,
                                              self.m_ship.getRegister(self.m_arg2).getValue(),
                                              BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_ry = self.m_ship.getRegister(self.m_arg2)
        l_value = l_rx.getValue() - l_ry.getValue()
        l_tmp = Register("tmp")
        l_tmp.setValue(l_value)
        self.m_ship.setS(l_tmp.isNeg())
        self.m_ship.setZ(l_tmp.isNull())
        p_data.append({
            "action" : "sz",
            "z"      : l_rx.isNull(),
            "s"      : l_rx.isNeg()
        })

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2) ]
