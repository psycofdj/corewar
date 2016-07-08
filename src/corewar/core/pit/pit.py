# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from pyscript.exceptions    import BaseException
from pyscript.logger.object import LoggingObject
from corewar.core.data.ship import Ship

# ---------------------------------------------------------------------------- #

class Pit(LoggingObject, object):
    def __init__(self):
        LoggingObject.__init__(self, "pit")
        self.registerHandler("lexer",  "[lexer]")
        self.registerHandler("parser", "[parser]")
        self.reset()

    def reset(self):
        self.m_error = 0
        self.m_codeSize = 0
        self.m_labels = {}
        self.m_owner = ""
        self.m_comment = ""
        self.m_instrList = []
        self.m_sourcePath = ""
        self.m_source = ""

    def overflow(self, p_instr, p_val, p_type):
        l_instrName = p_instr.__class__.__name__.lower()
        l_message = "constant '%s' overflows %s value in instruction '%s' at line %d"
        self.warning("parser", l_message, p_val, p_type, l_instrName, p_instr.getLine())

    def lexError(self, p_line, p_index, p_value):
        l_startCol = p_index - (self.m_source.rfind("\n", 0, p_index) + 1)
        self.error("lexer",
                   "%s: error: illegal character '%s' at line %d, col %d",
                   self.m_sourcePath,
                   p_value,
                   p_line,
                   l_startCol)
        self.incError()

    def parseError(self, p_line, p_index, p_value):
        l_startCol = p_index - (self.m_source.rfind("\n", 0, p_index) + 1)
        l_endCol = l_startCol + len(p_value)
        self.error("parser",
                   "%s: error: unexpected token '%s' at line %d, col %d-%d",
                   self.m_sourcePath,
                   p_value,
                   p_line,
                   l_startCol,
                   l_endCol)
        self.incError()

    def incError(self):
        self.m_error += 1

    def hasError(self):
        return (self.m_error > 0)

    def buildShipSource(self, p_sourcePath, p_id):
        try:
            l_file = open(p_sourcePath, "r")
            l_source = "".join(l_file.readlines())
            l_file.close()
        except:
            raise BaseException("unable to open file '%s'" % p_sourcePath, "pit")
        return self.buildShipCode(l_source, p_sourcePath, p_id)

    def buildShipCode(self, p_sourceCode, p_sourcePath = "<inline>", p_id = 0):
        self.reset()
        self.m_sourcePath = p_sourcePath
        self.m_source     = p_sourceCode
        from corewar.core.pit import grammar
        grammar.run_parser(self, self.m_source)
        if self.m_error != 0:
            return None
        return self.__build(p_id)

    def addInstruction(self, p_instr):
        self.m_codeSize += p_instr.getCodeSize()
        self.m_instrList.append(p_instr)

    def defineLabel(self, p_name, p_line):
        if p_name in self.m_labels:
            l_message = "erorr: label '%s' already defined at line %d"
            self.error("parser", l_message, p_name, p_line)
            self.incError()
        self.m_labels[p_name] = self.m_codeSize

    def evaluateLabel(self, p_name, p_line):
        if not p_name in self.m_labels:
            l_message = "error : undefined reference to label '%s' at line %d"
            self.error("parser", l_message, p_name, p_line)
            self.incError()
            return 0
        return self.m_labels[p_name]

    def setOwner(self, p_str):
        self.m_owner = p_str

    def setComment(self, p_str):
        self.m_comment = p_str

    def __build(self, p_id):
        l_ship = Ship(p_id)
        l_ship.setOwner(self.m_owner)
        l_ship.setComment(self.m_comment)
        for c_instr in self.m_instrList:
            c_instr.evaluate(self)
            l_quartets = c_instr.buildInstr()
            for c_quart in l_quartets:
                l_ship.addInitialCode(c_quart)
        return l_ship
