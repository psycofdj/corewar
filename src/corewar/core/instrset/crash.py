# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Crash(BaseInstruction):
    def __init__(self, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Crash, 1, 0b0000, None, p_line)

    def __str__(self):
        return  "crash : %s" % BaseInstruction.__str__(self)

    def doExecute(self, p_data):
        p_data.append({ "action" : "status", "value" : "crashed" })
        self.m_ship.setCrashed()

    def serializeArgs(self):
        return []
