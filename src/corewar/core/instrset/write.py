# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

import sys
from corewar.core.data          import const
from corewar.core.instrset.base import BaseInstruction
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet, Register

# ---------------------------------------------------------------------------- #

class Write(BaseInstruction):
    def __init__(self, p_arg1, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Write, 3, 0b1111, 0b1111, p_line)
        self.m_arg1 = p_arg1

    def __str__(self):
        return "write r%s(%d) : %s" % (self.m_arg1,
                                       self.m_ship.getRegister(self.m_arg1).getValue(),
                                       BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_tmp = Register(l_rx.getValue() & 0b0000000011111111)
        sys.stdout.write(str(l_tmp.getValue()))

    def serializeArgs(self):
        return [ Quartet(self.m_arg1) ]
