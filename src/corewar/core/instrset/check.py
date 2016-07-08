# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Check(BaseInstruction):
    def __init__(self, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Check, 2, 0xF, 0xC, p_line)

    def __str__(self):
        return  "check : %s" % (BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        self.m_ship.setCheckState(True)

    def serializeArgs(self):
        return []

