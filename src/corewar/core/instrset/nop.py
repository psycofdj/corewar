# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Nop(BaseInstruction):
    def __init__(self, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Nop, 1, 0b0001, None, p_line)

    def __str__(self):
        return "nop : %s" % (BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        pass

    def serializeArgs(self):
        return []


