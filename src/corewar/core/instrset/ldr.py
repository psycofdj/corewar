# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Ldr(BaseInstruction):
    def __init__(self, p_arg1, p_arg2, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Ldr, 3, 0b1101, None, p_line)
        self.m_arg1 = p_arg1
        self.m_arg2 = p_arg2
        self.m_readData = []

    def __str__(self):
        return  "ldr r%s [r%s(%d)] : %s" % (self.m_arg1,
                                            self.m_arg2,
                                            self.m_ship.getRegister(self.m_arg2).getValue(),
                                            BaseInstruction.__str__(self))

    def isFinished(self):
        return len(self.m_readData) == 4

    def doExecute(self, p_data):
        l_ry = self.m_ship.getRegister(self.m_arg2)
        l_offset = l_ry.getValue() + len(self.m_readData)
        l_chunk = self.m_circuit.getChunkFromShip(self.m_ship, l_offset)
        l_dataPart = l_chunk.getData().getValue()
        self.m_readData.append(l_dataPart)
        if self.m_readData == 4:
            l_rx = self.m_ship.getRegister(self.m_arg1)
            l_value = 0
            for c_idx in range(4):
                l_value += (self.m_readData[c_idx] << (c_idx * 4))
            l_rx.setValue(l_value)
            p_data.append({
                "action" : "register",
                "name"   : l_rx.getName(),
                "value"  : l_rx.getValue()
            })

    def serializeArgs(self):
        return [ Quartet(self.m_arg1), Quartet(self.m_arg2) ]
