# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Bz(BaseInstruction):
    def __init__(self, p_arg1, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Bz, 3, 0b1111, 0b1000, p_line)
        self.m_arg1 = p_arg1

    def __str__(self):
        return "bz r%s(%d) : %s" % (self.m_arg1,
                                    self.m_ship.getRegister(self.m_arg1).getValue(),
                                    BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_offset = l_rx.getValue()
        if self.m_ship.getZ():
            self.m_circuit.moveShip(self.m_ship, l_offset)

    def serializeArgs(self):
        return [ Quartet(self.m_arg1) ]

