# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

import os

from pyscript             import config
from ply                  import lex, yacc
from corewar.core.pit.pit import Pit
from corewar.core         import instrset

# ---------------------------------------------------------------------------- #

instructions = [
    'and', 'or', 'xor', 'not', 'rol', 'asr', 'add', 'sub',
    'cmp', 'addi', 'cmpi', 'neg', 'mov', 'swp', 'lc', 'll',
    'str', 'ldr', 'ldb', 'stb', 'b', 'bz', 'bnz', 'bs', 'write',
    'stat', 'check', 'mode', 'fork', 'crash', 'nop'
    ]

modes = [
    "feisar", "goteki45", "agsystems", "auricom", "assegai",
    "piranha", "qirex", "icaras", "rocket", "missile", "mine",
    "plasma"
    ]

tokens = [
    'LPAREN',
    'RPAREN',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    'MOD',
    'COMMA',
    'STRING',
    'HEX_DIGIT',
    'OCT_DIGIT',
    'DEC_DIGIT',
    'BIN_DIGIT',
    'DIRECTIVE',
    'REGISTER',
    'REGISTER_REF',
    'LABEL',
    'MODENAME',
    'LABELDECL',
    'COMMENT' ] + \
    [ x.upper() for x in instructions ]

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_COMMA = r'\,'
t_DIRECTIVE = r"(\.name)|(\.comment)"
t_MODENAME = "|".join(modes)
t_ignore = ' \t'

def t_STRING(t):
    r'"[^\"]*"'
    t.value = str(t.value[1:-1])
    return t

def t_REGISTER(t):
    r"r15|r14|r13|r12|r11|r10|r9|r8|r7|r6|r5|r4|r3|r2|r1|r0"
    t.value = int(t.value[1:])
    return t

def t_REGISTER_REF(t):
    r"\[r0\]|\[r1\]|\[r2\]|\[r3\]|\[r4\]|\[r5\]|\[r6\]|\[r7\]|\[r8\]|\[r9\]|\[r10\]|\[r11\]|\[r12\]|\[r13\]|\[r14\]|\[r15\]"
    t.value = int(t.value[2:-1])
    return t

def t_OCT_DIGIT(t):
    r"0[0-7]+([0-7_][0-7])*"
    l_val = t.value.replace("_", "")
    t.value = int(l_val, 8)
    return t

def t_HEX_DIGIT(t):
    r"0x[0-9a-fA-F]+([0-9a-fA-F_][0-9a-fA-F])*"
    l_val = t.value.replace("_", "")
    t.value = int(l_val, 16)
    return t

def t_DEC_DIGIT(t):
    r"[0-9]+([0-9_][0-9])*"
    l_val = t.value.replace("_", "")
    t.value = int(l_val, 10)
    return t

def t_BIN_DIGIT(t):
    r"%[0-1]+([0-1_][0-1])*"
    l_val = t.value.replace("_", "")
    l_val = l_val[1:]
    t.value = int(l_val, 2)
    return t

def t_LABELDECL(t):
    r"[a-zA-Z_0-9]+:"
    t.value = t.value[0:-1]
    return t

def t_LABEL(t):
    r"[a-zA-Z_0-9]+"
    if t.value.lower() in instructions:
        t.type = t.value.upper()
        t.value = t.value.lower()
    elif t.value.lower() in modes:
        t.type = 'MODENAME'
        t.value = t.value.lower()
    return t

def t_COMMENT(t):
    r"\#.*"
    t.value = str(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.pit.lexError(t.lexer.lineno, t.lexer.lexpos, t.value[0])
    t.lexer.skip(1)



precedence = (
    ('left','PLUS','MINUS'),
    ('left','MUL','DIV', 'MOD'),
    ('right','UMINUS', 'UPLUS')
    )

def p_initial(t):
    '''global :
              | global statement'''

def p_statement(t):
    '''statement : directive
                 | comment
                 | instruction
                 | labeldecl'''

def p_statement_comment(t):
    ''' comment : COMMENT'''

def p_statement_directive(t):
    ''' directive : DIRECTIVE STRING'''

    l_name = t[1]
    l_val  = t[2]
    if l_name == ".comment":
        t.lexer.pit.setComment(l_val)
    if l_name == ".name":
        t.lexer.pit.setOwner(l_val)

def p_statement_instruction(t):
    ''' instruction : crash_instr
                    | nop_instr
                    | check_instr
                    | fork_instr
                    | mode_instr
                    | b_instr
                    | bz_instr
                    | bnz_instr
                    | bs_instr
                    | and_instr
                    | or_instr
                    | xor_instr
                    | not_instr
                    | add_instr
                    | sub_instr
                    | cmp_instr
                    | neg_instr
                    | mov_instr
                    | swp_instr
                    | stat_instr
                    | cmpi_instr
                    | addi_instr
                    | rol_instr
                    | asr_instr
                    | lc_instr
                    | ll_instr
                    | ldr_instr
                    | str_instr
                    | ldb_instr
                    | stb_instr
                    | write_instr '''
    t.lexer.pit.addInstruction(t[1])

def p_statement_instruction_crash(t):
    "crash_instr : CRASH"
    l_line = t.lineno(1)
    t[0] = instrset.crash.Crash(l_line)

def p_statement_instruction_nop(t):
    "nop_instr : NOP"
    l_line = t.lineno(1)
    t[0] = instrset.nop.Nop(l_line)

def p_statement_instruction_check(t):
    "check_instr : CHECK"
    l_line = t.lineno(1)
    t[0] = instrset.check.Check(l_line)

def p_statement_instruction_fork(t):
    "fork_instr : FORK"
    l_line = t.lineno(1)
    t[0] = instrset.fork.Fork(l_line)

def p_statement_instruction_mode(t):
    "mode_instr : MODE MODENAME"
    l_val = t[2]
    l_line = t.lineno(1)
    t[0] = instrset.mode.Mode(l_val, l_line)

def p_statement_instruction_b(t):
    "b_instr : B REGISTER"
    l_reg = t[2]
    l_line = t.lineno(1)
    t[0] = instrset.b.B(l_reg, l_line)

def p_statement_instruction_bz(t):
    "bz_instr : BZ REGISTER"
    l_reg = t[2]
    l_line = t.lineno(1)
    t[0] = instrset.bz.Bz(l_reg, l_line)

def p_statement_instruction_bnz(t):
    "bnz_instr : BNZ REGISTER"
    l_reg = t[2]
    l_line = t.lineno(1)
    t[0] = instrset.bnz.Bnz(l_reg, l_line)

def p_statement_instruction_bs(t):
    "bs_instr : BS REGISTER"
    l_reg = t[2]
    l_line = t.lineno(1)
    t[0] = instrset.bs.Bs(l_reg, l_line)

def p_statement_instruction_and(t):
    "and_instr : AND REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.andi.And(l_rx, l_ry, l_line)

def p_statement_instruction_or(t):
    "or_instr : OR REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.ori.Or(l_rx, l_ry, l_line)

def p_statement_instruction_xor(t):
    "xor_instr : XOR REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.xor.Xor(l_rx, l_ry, l_line)

def p_statement_instruction_not(t):
    "not_instr : NOT REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.noti.Not(l_rx, l_ry, l_line)

def p_statement_instruction_add(t):
    "add_instr : ADD REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.add.Add(l_rx, l_ry, l_line)

def p_statement_instruction_sub(t):
    "sub_instr : SUB REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.sub.Sub(l_rx, l_ry, l_line)

def p_statement_instruction_cmp(t):
    "cmp_instr : CMP REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.cmp.Cmp(l_rx, l_ry, l_line)

def p_statement_instruction_neg(t):
    "neg_instr : NEG REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.neg.Neg(l_rx, l_ry, l_line)

def p_statement_instruction_mov(t):
    "mov_instr : MOV REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.mov.Mov(l_rx, l_ry, l_line)

def p_statement_instruction_swp(t):
    "swp_instr : SWP REGISTER COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.swp.Swp(l_rx, l_ry, l_line)

def p_statement_instruction_stat(t):
    "stat_instr : STAT REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.stat.Stat(l_rx, l_n, l_line)

def p_statement_instruction_cmpi(t):
    "cmpi_instr : CMPI REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.cmpi.Cmpi(l_rx, l_n, l_line)

def p_statement_instruction_addi(t):
    "addi_instr : ADDI REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.addi.Addi(l_rx, l_n, l_line)

def p_statement_instruction_rol(t):
    "rol_instr : ROL REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.rol.Rol(l_rx, l_n, l_line)

def p_statement_instruction_asr(t):
    "asr_instr : ASR REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.asr.Asr(l_rx, l_n, l_line)

def p_statement_instruction_lc(t):
    "lc_instr : LC REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.lc.Lc(l_rx, l_n, None, l_line)

def p_statement_instruction_ll(t):
    "ll_instr : LL REGISTER COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.ll.Ll(l_rx, l_n, None, None, None, l_line)

def p_statement_instruction_ldr(t):
    "ldr_instr : LDR REGISTER COMMA REGISTER_REF"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.ldr.Ldr(l_rx, l_ry, l_line)

def p_statement_instruction_str(t):
    "str_instr : STR REGISTER_REF COMMA REGISTER"
    l_rx = t[2]
    l_ry = t[4]
    l_line = t.lineno(1)
    t[0] = instrset.str.Str(l_rx, l_ry, l_line)

def p_statement_instruction_ldb(t):
    "ldb_instr : LDB REGISTER_REF COMMA expression COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_m = t[6]
    l_line = t.lineno(1)
    t[0] = instrset.ldb.Ldb(l_rx, l_n, None, l_m, None, l_line)

def p_statement_instruction_stb(t):
    "stb_instr : STB REGISTER_REF COMMA expression COMMA expression"
    l_rx = t[2]
    l_n = t[4]
    l_m = t[6]
    l_line = t.lineno(1)
    t[0] = instrset.stb.Stb(l_rx, l_n, None, l_m, None, l_line)

def p_statement_instruction_write(t):
    "write_instr : WRITE REGISTER"
    l_n = t[2]
    l_line = t.lineno(1)
    t[0] = instrset.write.Write(l_n, l_line)

def p_statement_labeldecl(t):
    ''' labeldecl : LABELDECL'''
    l_val = t[1]
    l_lineno = t.lineno(1)
    t.lexer.pit.defineLabel(l_val, l_lineno)

def p_expression_label(t):
    '''expression : LABEL'''
    l_labelName = t[1]
    l_lineno = t.lineno(1)
    t[0] = lambda: t.lexer.pit.evaluateLabel(l_labelName, l_lineno)

def p_expression_number(t):
    '''expression : HEX_DIGIT
                  | DEC_DIGIT
                  | OCT_DIGIT
                  | BIN_DIGIT'''
    l_value = t[1]
    t[0] = lambda : l_value

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression MOD expression'''
    l_val1 = t[1]
    l_val2 = t[3]
    if   t[2] == '+': t[0] = lambda : l_val1() + l_val2()
    elif t[2] == '-': t[0] = lambda : l_val1() - l_val2()
    elif t[2] == '*': t[0] = lambda : l_val1() * l_val2()
    elif t[2] == '/': t[0] = lambda : l_val1() / l_val2()

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    l_val = t[2]
    t[0] = lambda : 0 - l_val()

def p_expression_uplus(t):
    'expression : PLUS expression %prec UPLUS'
    l_val = t[2]
    t[0] = lambda : l_val()

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    l_val = t[2]
    t[0] = lambda : l_val()

def p_error(t):
    t.lexer.pit.parseError(t.lineno, t.lexpos, str(t.value))




def run_parser(pit, source):
    l_lexer      = lex.lex()
    l_parser     = yacc.yacc(tabmodule="parsetab", outputdir=config.get("general", "tmp-dir"), debug=0)
    l_lexer.pit  = pit
    l_parser.pit = pit
    l_parser.parse(source.encode("utf-8"), tracking=True)
