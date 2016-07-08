# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Stat(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Stat, 4, 0b1111, 0b1011, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2


    def __str__(self):
        return  "stat r%s %d : %s" % (self.m_arg1,
                                      self.m_arg2,
                                      BaseInstruction.__str__(self))

    def doExecute(self, p_data):
        l_rx = self.m_ship.getRegister(self.m_arg1)
        l_n  = self.m_arg2
        if l_n == 1:
            l_rx.setValue(self.m_ship.getMode().Value)
        elif l_n == 2:
            l_rx.setValue(self.m_ship.getPC())
        elif l_n == 3:
            l_rx.setValue(self.m_ship.getWO())
        elif l_n == 4:
            l_rx.setValue((self.m_ship.getLastCheckWO() / const.CHECKPOINT_SIZE) + 1)
        elif l_n == 5:
            l_rx.setValue(self.m_ship.getInitialPC())
        elif l_n == 6:
            l_rx.setValue(const.MEMORY_SIZE)
        elif l_n == 7:
            l_rx.setValue(const.LAPS_NUMBER)
        elif l_n == 8:
            l_rx.setValue(const.CHECKPOINTS_PER_LAP)
        elif l_n == 9:
            l_rx.setValue(const.CHECKPOINT_SIZE)
        elif l_n == 10:
            l_rx.setValue(const.CHECKPOINT_DELAY)
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
        if (l_n < 0) or (l_n > 10):
            p_pit.overflow(self, l_n, "[0-10]")
        self.m_arg2 = l_n

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2) ]
