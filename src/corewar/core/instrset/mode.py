# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data          import const
from corewar.core.data.modes    import Modes
from corewar.core.data.quartet  import Quartet
from corewar.core.instrset.base import BaseInstruction

# ---------------------------------------------------------------------------- #

class Mode(BaseInstruction):
    def __init__(self, p_arg1, p_line = 0):
        BaseInstruction.__init__(self, Modes.Instr.Mode, 3, 0b1111, 0b1101, p_line)
        self.m_arg1 = p_arg1

    def __str__(self):
        return  "mode %s : %s" % (self.idxToMode(self.m_arg1).Name,
                                  BaseInstruction.__str__(self))

    def idxToModeName(self, p_idx):
        if p_idx == 0:    return "Feisar"
        elif p_idx == 1:  return "Goteki45"
        elif p_idx == 2:  return "Agsystems"
        elif p_idx == 3:  return "Auricom"
        elif p_idx == 4:  return "Assegai"
        elif p_idx == 5:  return "Piranha"
        elif p_idx == 6:  return "Qirex"
        elif p_idx == 7:  return "Icaras"
        elif p_idx == 8:  return "Rocket"
        elif p_idx == 9:  return "Missile"
        elif p_idx == 10: return "Mine"
        elif p_idx == 11: return "Plasma"
        return None

    def modeNameToIdx(self, p_name):
        if   p_name == "feisar":    return 0
        elif p_name == "goteki45":  return 1
        elif p_name == "agsystems": return 2
        elif p_name == "auricom":   return 3
        elif p_name == "assegai":   return 4
        elif p_name == "piranha":   return 5
        elif p_name == "qirex":     return 6
        elif p_name == "icaras":    return 7
        elif p_name == "rocket":    return 8
        elif p_name == "missile":   return 9
        elif p_name == "mine":      return 10
        elif p_name == "plasma":    return 11
        return None

    def idxToMode(self, p_idx):
        if p_idx == 0:    return Modes.Feisar
        elif p_idx == 1:  return Modes.Goteki45
        elif p_idx == 2:  return Modes.Agsystems
        elif p_idx == 3:  return Modes.Auricom
        elif p_idx == 4:  return Modes.Assegai
        elif p_idx == 5:  return Modes.Piranha
        elif p_idx == 6:  return Modes.Qirex
        elif p_idx == 7:  return Modes.Icaras
        elif p_idx == 8:  return Modes.Rocket
        elif p_idx == 9:  return Modes.Missile
        elif p_idx == 10: return Modes.Mine
        elif p_idx == 11: return Modes.Plasma
        return None

    def doExecute(self, p_data):
        l_n  = self.m_arg1
        l_mode = self.idxToMode(l_n)
        if l_mode != None:
            self.m_ship.setMode(l_mode)
            p_data.append({ "action" : "mode", "value" : self.idxToModeName(l_n) })


    def evaluate(self, p_pit):
        l_idx = self.modeNameToIdx(self.m_arg1)
        if l_idx == None:
            p_pit.overflow(self, self.m_arg1, "(modename)")
            self.m_arg1 = 0
        else:
            self.m_arg1 = l_idx

    def serializeArgs(self):
        return [ Quartet(self.m_arg1) ]

