# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data     import const
from corewar.core.instrset import *
from pyscript.exceptions   import BaseException

# ---------------------------------------------------------------------------- #

class Decoder(object):
    def decode(self, p_ship, p_circuit, p_cycle):
        l_queue = p_ship.getQueue()
        l_handler = getattr(self, "decodeSz%d" % len(l_queue))
        l_instr = l_handler(l_queue)
        if l_instr == None:
            return None
        l_isBlueArrow = (l_queue[0].getID() % const.BLUE_ARROW_SPACING == 0)

        l_isRail = (l_queue[0].getWroteLastCycle() == (p_cycle - 1))
        if l_queue[0].getValue() == 0b1111:
            l_isRail = l_isRail or (l_queue[1].getWroteLastCycle() == (p_cycle - 1))

        l_instr.setBlueArrowState(l_isBlueArrow)
        l_instr.setRailState(l_isRail)
        l_instr.setShip(p_ship)
        l_instr.setCircuit(p_circuit)
        return l_instr

    def decodeSz0(self, p_queue):
        return None

    def decodeSz1(self, p_queue):
        if p_queue[0].getValue() == 0b0000:
            return crash.Crash()
        elif p_queue[0].getValue() == 0b0001:
            return nop.Nop()
        return None

    def decodeSz2(self, p_queue):
        if p_queue[0].getValue() == 0b1111:
            if p_queue[1].getValue() == 0b1100:
                return check.Check()
            elif p_queue[1].getValue() == 0b1110:
                return fork.Fork()
        return None

    def decodeSz3(self, p_queue):
        if p_queue[0].getValue() == 0b1111:
            if p_queue[1].getValue() == 0b0111:
                return b.B(p_queue[2].getValue())
            elif p_queue[1].getValue() == 0b1000:
                return bz.Bz(p_queue[2].getValue())
            elif p_queue[1].getValue() == 0b1001:
                return bnz.Bnz(p_queue[2].getValue())
            elif p_queue[1].getValue() == 0b1010:
                return bs.Bs(p_queue[2].getValue())
            elif p_queue[1].getValue() == 0b1101:
                return mode.Mode(p_queue[2].getValue())
            elif p_queue[1].getValue() == 0b1111:
                return write.Write(p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b0010:
            return andi.And(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b0011:
            return ori.Or(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b0100:
            return xor.Xor(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b0101:
            return noti.Not(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b0110:
            return rol.Rol(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b0111:
            return asr.Asr(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1000:
            return add.Add(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1001:
            return sub.Sub(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1010:
            return cmp.Cmp(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1011:
            return neg.Neg(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1100:
            return mov.Mov(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1101:
            return ldr.Ldr(p_queue[1].getValue(), p_queue[2].getValue())
        elif p_queue[0].getValue() == 0b1110:
            return str.Str(p_queue[1].getValue(), p_queue[2].getValue())
        return None

    def decodeSz4(self, p_queue):
        if p_queue[0].getValue() == 0b1111:
            if p_queue[1].getValue() == 0b0100:
                return swp.Swp(p_queue[2].getValue(), p_queue[3].getValue())
            if p_queue[1].getValue() == 0b0101:
                return addi.Addi(p_queue[2].getValue(), p_queue[3].getValue())
            if p_queue[1].getValue() == 0b0110:
                return cmpi.Cmpi(p_queue[2].getValue(), p_queue[3].getValue())
            if p_queue[1].getValue() == 0b1011:
                return stat.Stat(p_queue[2].getValue(), p_queue[3].getValue())
        return None

    def decodeSz5(self, p_queue):
        if p_queue[0].getValue() == 0b1111:
            if p_queue[1].getValue() == 0b0010:
                return lc.Lc(p_queue[2].getValue(),
                                       p_queue[3].getValue(),
                                       p_queue[4].getValue())
        return None

    def decodeSz6(self, p_queue):
        return None

    def decodeSz7(self, p_queue):
        if p_queue[0].getValue() == 0b1111:
            if p_queue[1].getValue() == 0b0000:
                return ldb.Ldb(p_queue[2].getValue(),
                               p_queue[3].getValue(),
                               p_queue[4].getValue(),
                               p_queue[5].getValue(),
                               p_queue[6].getValue())
            elif p_queue[1].getValue() == 0b0001:
                return stb.Stb(p_queue[2].getValue(),
                               p_queue[3].getValue(),
                               p_queue[4].getValue(),
                               p_queue[5].getValue(),
                               p_queue[6].getValue())
            elif p_queue[1].getValue() == 0b0011:
                return ll.Ll(p_queue[2].getValue(),
                             p_queue[3].getValue(),
                             p_queue[4].getValue(),
                             p_queue[5].getValue(),
                             p_queue[6].getValue())
        raise BaseException("error 7 length queue could not be decoded", "instructions")

