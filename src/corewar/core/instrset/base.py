# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from pyscript.exceptions       import BaseException
from corewar.core.data.quartet import Quartet

# ---------------------------------------------------------------------------- #

class BaseInstruction:
    def __init__(self, p_instrIdx, p_codeSize, p_optcode1, p_optcode2, p_line):
        self.m_instrIdx = p_instrIdx
        self.m_ship = None
        self.m_line = p_line
        self.m_circuit = None
        self.m_blueArrowState = False
        self.m_railState = False
        self.m_codeSize = p_codeSize
        self.m_optCodes = [ Quartet(p_optcode1) ]
        if p_optcode2 != None:
            self.m_optCodes.append(Quartet(p_optcode2))

    def __str__(self):
        return "blue = %s, rail = %s" % (self.m_blueArrowState, self.m_railState)

    def getLine(self):
        return self.m_line

    def evaluate(self, p_pit):
        pass

    def getCodeSize(self):
        return self.m_codeSize

    def getDecodeDelay(self):
        l_delay = self.m_ship.getMode().Decode[self.m_instrIdx]
        if self.m_blueArrowState:
            l_delay /= 2
        if self.m_railState:
            l_delay /= 2
        return l_delay

    def getExecuteDelay(self):
        l_delay = self.m_ship.getMode().Execute[self.m_instrIdx]
        if self.m_blueArrowState:
            l_delay /= 2
        if self.m_railState:
            l_delay /= 2
        return l_delay

    def isFinished(self):
        return True

    def doExecute(self, p_data):
        raise BaseException("instruction not implemented", "instruction")

    def serializeArgs(self):
        raise BaseException("instruction not implemented", "instruction")

    def buildInstr(self):
        return self.m_optCodes + self.serializeArgs()

    def setShip(self, p_ship):
        self.m_ship = p_ship
    def setCircuit(self, p_circuit):
        self.m_circuit = p_circuit
    def setBlueArrowState(self, p_state):
        self.m_blueArrowState = p_state
    def setRailState(self, p_state):
        self.m_railState = p_state
