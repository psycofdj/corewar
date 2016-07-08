# -*- coding: utf-8
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #

class Quartet:
    def __init__(self, p_value = 0):
        self.m_bits = [ False for x in range(4) ]
        for c_idx in range(4):
            self.setBit(c_idx, (p_value >> c_idx) & 0b0001 != 0)

    def __str__(self):
        return "[%s]" % ",".join([ "1" if x else "0" for x in reversed(self.m_bits) ])

    def getBit(self, p_bit):
        return self.m_bits[p_bit]

    def setBit(self, p_bit, p_value):
        self.m_bits[p_bit] = bool(p_value)

    def copy(self, p_quartet):
        for c_bit in reversed(range(4)):
            self.m_bits[c_bit] = p_quartet.getBit(c_bit)

    def getValue(self):
        l_value = 0
        for c_idx in range(4):
            if self.m_bits[c_idx]:
                l_value += 2 ** c_idx
        return l_value

    def setValue(self, p_value):
        self.setBit(1, (p_value & 0b0001))
        self.setBit(2, (p_value & 0b0010) >> 1)
        self.setBit(3, (p_value & 0b0100) >> 2)
        self.setBit(4, (p_value & 0b1000) >> 3)


class Register:
    def __init__(self, p_name, p_value = 0):
        self.m_name = p_name;
        self.setValue(p_value)

    def __str__(self):
        l_value = self.getValue()
        l_n0 = (l_value & 0b0000000000001111)
        l_n1 = (l_value & 0b0000000011110000) >> 4
        l_n2 = (l_value & 0b0000111100000000) >> 8
        l_n3 = (l_value & 0b1111000000000000) >> 12
        return ",".join([ str(x) for x in [ Quartet(l_n0),
                                            Quartet(l_n1),
                                            Quartet(l_n2),
                                            Quartet(l_n3)]
                          ])

    def getName(self):
        return self.m_name

    def getValue(self):
        return self.m_value

    def setValue(self, p_value):
        if ((p_value & 0b1000000000000000) >> 15) == 1:
            p_value = p_value | -32768
        else:
            p_value = p_value & 32767
        self.m_value = p_value

    def isNeg(self):
        return self.m_value < 0

    def isNull(self):
        return self.m_value == 0
