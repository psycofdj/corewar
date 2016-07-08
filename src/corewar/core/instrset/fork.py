# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.instrset.base import BaseInstruction
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet

# ---------------------------------------------------------------------------- #

class Fork(BaseInstruction):
    def __init__(self, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Fork, 2, 0xF, 0xE, p_line)

    def __str__(self):
        return  "fork : %s" % (BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        self.m_ship.setForkState(True)

    def serializeArgs(self):
        return []
