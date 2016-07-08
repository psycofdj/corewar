# -*- coding: utf-8
# ---------------------------------------------------------------------------- #

from corewar.core.data import const

# ---------------------------------------------------------------------------- #


class Modes:
    class Instr:
        Crash = 0
        Fork  = 1
        Mode  = 2
        Check = 3
        Stat  = 4
        Write = 5
        Stb   = 6
        Ldb   = 7
        Str   = 8
        Ldr   = 9
        Ll    = 10
        Lc    = 11
        Mov   = 12
        Nop   = 13
        Bs    = 14
        Bnz   = 15
        Bz    = 16
        B     = 17
        Swp   = 18
        Rol   = 19
        Not   = 20
        Xor   = 21
        Or    = 22
        And   = 23
        Neg   = 24
        Asr   = 25
        Cmpi  = 26
        Addi  = 27
        Cmp   = 28
        Sub   = 29
        Add   = 30

    class Feisar:
        Name = "Feisar"
        Sight = const.IDX_MOD_FEISAR
        Execute = [ const.DELAY_EXECUTE_CRASH_FEISAR, const.DELAY_EXECUTE_FORK_FEISAR,
                    const.DELAY_EXECUTE_MODE_FEISAR,  const.DELAY_EXECUTE_CHECK_FEISAR,
                    const.DELAY_EXECUTE_STAT_FEISAR,  const.DELAY_EXECUTE_WRITE_FEISAR,
                    const.DELAY_EXECUTE_STB_FEISAR,   const.DELAY_EXECUTE_LDB_FEISAR,
                    const.DELAY_EXECUTE_STR_FEISAR,   const.DELAY_EXECUTE_LDR_FEISAR,
                    const.DELAY_EXECUTE_LL_FEISAR,    const.DELAY_EXECUTE_LC_FEISAR,
                    const.DELAY_EXECUTE_MOV_FEISAR,   const.DELAY_EXECUTE_NOP_FEISAR,
                    const.DELAY_EXECUTE_BS_FEISAR,    const.DELAY_EXECUTE_BNZ_FEISAR,
                    const.DELAY_EXECUTE_BZ_FEISAR,    const.DELAY_EXECUTE_B_FEISAR,
                    const.DELAY_EXECUTE_SWP_FEISAR,   const.DELAY_EXECUTE_ROL_FEISAR,
                    const.DELAY_EXECUTE_NOT_FEISAR,   const.DELAY_EXECUTE_XOR_FEISAR,
                    const.DELAY_EXECUTE_OR_FEISAR,    const.DELAY_EXECUTE_AND_FEISAR,
                    const.DELAY_EXECUTE_NEG_FEISAR,   const.DELAY_EXECUTE_ASR_FEISAR,
                    const.DELAY_EXECUTE_CMPI_FEISAR,  const.DELAY_EXECUTE_ADDI_FEISAR,
                    const.DELAY_EXECUTE_CMP_FEISAR,   const.DELAY_EXECUTE_SUB_FEISAR,
                    const.DELAY_EXECUTE_ADD_FEISAR ]
        Decode = [ const.DELAY_DECODE_CRASH_FEISAR, const.DELAY_DECODE_FORK_FEISAR,
                    const.DELAY_DECODE_MODE_FEISAR,  const.DELAY_DECODE_CHECK_FEISAR,
                    const.DELAY_DECODE_STAT_FEISAR,  const.DELAY_DECODE_WRITE_FEISAR,
                    const.DELAY_DECODE_STB_FEISAR,   const.DELAY_DECODE_LDB_FEISAR,
                    const.DELAY_DECODE_STR_FEISAR,   const.DELAY_DECODE_LDR_FEISAR,
                    const.DELAY_DECODE_LL_FEISAR,    const.DELAY_DECODE_LC_FEISAR,
                    const.DELAY_DECODE_MOV_FEISAR,   const.DELAY_DECODE_NOP_FEISAR,
                    const.DELAY_DECODE_BS_FEISAR,    const.DELAY_DECODE_BNZ_FEISAR,
                    const.DELAY_DECODE_BZ_FEISAR,    const.DELAY_DECODE_B_FEISAR,
                    const.DELAY_DECODE_SWP_FEISAR,   const.DELAY_DECODE_ROL_FEISAR,
                    const.DELAY_DECODE_NOT_FEISAR,   const.DELAY_DECODE_XOR_FEISAR,
                    const.DELAY_DECODE_OR_FEISAR,    const.DELAY_DECODE_AND_FEISAR,
                    const.DELAY_DECODE_NEG_FEISAR,   const.DELAY_DECODE_ASR_FEISAR,
                    const.DELAY_DECODE_CMPI_FEISAR,  const.DELAY_DECODE_ADDI_FEISAR,
                    const.DELAY_DECODE_CMP_FEISAR,   const.DELAY_DECODE_SUB_FEISAR,
                    const.DELAY_DECODE_ADD_FEISAR ]

    class Goteki45:
        Name = "Goteki45"
        Sight = const.IDX_MOD_GOTEKI45
        Execute = [ const.DELAY_EXECUTE_CRASH_GOTEKI45, const.DELAY_EXECUTE_FORK_GOTEKI45,
                    const.DELAY_EXECUTE_MODE_GOTEKI45,  const.DELAY_EXECUTE_CHECK_GOTEKI45,
                    const.DELAY_EXECUTE_STAT_GOTEKI45,  const.DELAY_EXECUTE_WRITE_GOTEKI45,
                    const.DELAY_EXECUTE_STB_GOTEKI45,   const.DELAY_EXECUTE_LDB_GOTEKI45,
                    const.DELAY_EXECUTE_STR_GOTEKI45,   const.DELAY_EXECUTE_LDR_GOTEKI45,
                    const.DELAY_EXECUTE_LL_GOTEKI45,    const.DELAY_EXECUTE_LC_GOTEKI45,
                    const.DELAY_EXECUTE_MOV_GOTEKI45,   const.DELAY_EXECUTE_NOP_GOTEKI45,
                    const.DELAY_EXECUTE_BS_GOTEKI45,    const.DELAY_EXECUTE_BNZ_GOTEKI45,
                    const.DELAY_EXECUTE_BZ_GOTEKI45,    const.DELAY_EXECUTE_B_GOTEKI45,
                    const.DELAY_EXECUTE_SWP_GOTEKI45,   const.DELAY_EXECUTE_ROL_GOTEKI45,
                    const.DELAY_EXECUTE_NOT_GOTEKI45,   const.DELAY_EXECUTE_XOR_GOTEKI45,
                    const.DELAY_EXECUTE_OR_GOTEKI45,    const.DELAY_EXECUTE_AND_GOTEKI45,
                    const.DELAY_EXECUTE_NEG_GOTEKI45,   const.DELAY_EXECUTE_ASR_GOTEKI45,
                    const.DELAY_EXECUTE_CMPI_GOTEKI45,  const.DELAY_EXECUTE_ADDI_GOTEKI45,
                    const.DELAY_EXECUTE_CMP_GOTEKI45,   const.DELAY_EXECUTE_SUB_GOTEKI45,
                    const.DELAY_EXECUTE_ADD_GOTEKI45 ]
        Decode = [ const.DELAY_DECODE_CRASH_GOTEKI45, const.DELAY_DECODE_FORK_GOTEKI45,
                    const.DELAY_DECODE_MODE_GOTEKI45,  const.DELAY_DECODE_CHECK_GOTEKI45,
                    const.DELAY_DECODE_STAT_GOTEKI45,  const.DELAY_DECODE_WRITE_GOTEKI45,
                    const.DELAY_DECODE_STB_GOTEKI45,   const.DELAY_DECODE_LDB_GOTEKI45,
                    const.DELAY_DECODE_STR_GOTEKI45,   const.DELAY_DECODE_LDR_GOTEKI45,
                    const.DELAY_DECODE_LL_GOTEKI45,    const.DELAY_DECODE_LC_GOTEKI45,
                    const.DELAY_DECODE_MOV_GOTEKI45,   const.DELAY_DECODE_NOP_GOTEKI45,
                    const.DELAY_DECODE_BS_GOTEKI45,    const.DELAY_DECODE_BNZ_GOTEKI45,
                    const.DELAY_DECODE_BZ_GOTEKI45,    const.DELAY_DECODE_B_GOTEKI45,
                    const.DELAY_DECODE_SWP_GOTEKI45,   const.DELAY_DECODE_ROL_GOTEKI45,
                    const.DELAY_DECODE_NOT_GOTEKI45,   const.DELAY_DECODE_XOR_GOTEKI45,
                    const.DELAY_DECODE_OR_GOTEKI45,    const.DELAY_DECODE_AND_GOTEKI45,
                    const.DELAY_DECODE_NEG_GOTEKI45,   const.DELAY_DECODE_ASR_GOTEKI45,
                    const.DELAY_DECODE_CMPI_GOTEKI45,  const.DELAY_DECODE_ADDI_GOTEKI45,
                    const.DELAY_DECODE_CMP_GOTEKI45,   const.DELAY_DECODE_SUB_GOTEKI45,
                    const.DELAY_DECODE_ADD_GOTEKI45 ]

    class Agsystems:
        Name = "Agsystems"
        Sight = const.IDX_MOD_AGSYSTEMS
        Execute = [ const.DELAY_EXECUTE_CRASH_AGSYSTEMS, const.DELAY_EXECUTE_FORK_AGSYSTEMS,
                    const.DELAY_EXECUTE_MODE_AGSYSTEMS,  const.DELAY_EXECUTE_CHECK_AGSYSTEMS,
                    const.DELAY_EXECUTE_STAT_AGSYSTEMS,  const.DELAY_EXECUTE_WRITE_AGSYSTEMS,
                    const.DELAY_EXECUTE_STB_AGSYSTEMS,   const.DELAY_EXECUTE_LDB_AGSYSTEMS,
                    const.DELAY_EXECUTE_STR_AGSYSTEMS,   const.DELAY_EXECUTE_LDR_AGSYSTEMS,
                    const.DELAY_EXECUTE_LL_AGSYSTEMS,    const.DELAY_EXECUTE_LC_AGSYSTEMS,
                    const.DELAY_EXECUTE_MOV_AGSYSTEMS,   const.DELAY_EXECUTE_NOP_AGSYSTEMS,
                    const.DELAY_EXECUTE_BS_AGSYSTEMS,    const.DELAY_EXECUTE_BNZ_AGSYSTEMS,
                    const.DELAY_EXECUTE_BZ_AGSYSTEMS,    const.DELAY_EXECUTE_B_AGSYSTEMS,
                    const.DELAY_EXECUTE_SWP_AGSYSTEMS,   const.DELAY_EXECUTE_ROL_AGSYSTEMS,
                    const.DELAY_EXECUTE_NOT_AGSYSTEMS,   const.DELAY_EXECUTE_XOR_AGSYSTEMS,
                    const.DELAY_EXECUTE_OR_AGSYSTEMS,    const.DELAY_EXECUTE_AND_AGSYSTEMS,
                    const.DELAY_EXECUTE_NEG_AGSYSTEMS,   const.DELAY_EXECUTE_ASR_AGSYSTEMS,
                    const.DELAY_EXECUTE_CMPI_AGSYSTEMS,  const.DELAY_EXECUTE_ADDI_AGSYSTEMS,
                    const.DELAY_EXECUTE_CMP_AGSYSTEMS,   const.DELAY_EXECUTE_SUB_AGSYSTEMS,
                    const.DELAY_EXECUTE_ADD_AGSYSTEMS ]
        Decode = [ const.DELAY_DECODE_CRASH_AGSYSTEMS, const.DELAY_DECODE_FORK_AGSYSTEMS,
                    const.DELAY_DECODE_MODE_AGSYSTEMS,  const.DELAY_DECODE_CHECK_AGSYSTEMS,
                    const.DELAY_DECODE_STAT_AGSYSTEMS,  const.DELAY_DECODE_WRITE_AGSYSTEMS,
                    const.DELAY_DECODE_STB_AGSYSTEMS,   const.DELAY_DECODE_LDB_AGSYSTEMS,
                    const.DELAY_DECODE_STR_AGSYSTEMS,   const.DELAY_DECODE_LDR_AGSYSTEMS,
                    const.DELAY_DECODE_LL_AGSYSTEMS,    const.DELAY_DECODE_LC_AGSYSTEMS,
                    const.DELAY_DECODE_MOV_AGSYSTEMS,   const.DELAY_DECODE_NOP_AGSYSTEMS,
                    const.DELAY_DECODE_BS_AGSYSTEMS,    const.DELAY_DECODE_BNZ_AGSYSTEMS,
                    const.DELAY_DECODE_BZ_AGSYSTEMS,    const.DELAY_DECODE_B_AGSYSTEMS,
                    const.DELAY_DECODE_SWP_AGSYSTEMS,   const.DELAY_DECODE_ROL_AGSYSTEMS,
                    const.DELAY_DECODE_NOT_AGSYSTEMS,   const.DELAY_DECODE_XOR_AGSYSTEMS,
                    const.DELAY_DECODE_OR_AGSYSTEMS,    const.DELAY_DECODE_AND_AGSYSTEMS,
                    const.DELAY_DECODE_NEG_AGSYSTEMS,   const.DELAY_DECODE_ASR_AGSYSTEMS,
                    const.DELAY_DECODE_CMPI_AGSYSTEMS,  const.DELAY_DECODE_ADDI_AGSYSTEMS,
                    const.DELAY_DECODE_CMP_AGSYSTEMS,   const.DELAY_DECODE_SUB_AGSYSTEMS,
                    const.DELAY_DECODE_ADD_AGSYSTEMS ]

    class Auricom:
        Name = "Auricom"
        Sight = const.IDX_MOD_AURICOM
        Execute = [ const.DELAY_EXECUTE_CRASH_AURICOM, const.DELAY_EXECUTE_FORK_AURICOM,
                    const.DELAY_EXECUTE_MODE_AURICOM,  const.DELAY_EXECUTE_CHECK_AURICOM,
                    const.DELAY_EXECUTE_STAT_AURICOM,  const.DELAY_EXECUTE_WRITE_AURICOM,
                    const.DELAY_EXECUTE_STB_AURICOM,   const.DELAY_EXECUTE_LDB_AURICOM,
                    const.DELAY_EXECUTE_STR_AURICOM,   const.DELAY_EXECUTE_LDR_AURICOM,
                    const.DELAY_EXECUTE_LL_AURICOM,    const.DELAY_EXECUTE_LC_AURICOM,
                    const.DELAY_EXECUTE_MOV_AURICOM,   const.DELAY_EXECUTE_NOP_AURICOM,
                    const.DELAY_EXECUTE_BS_AURICOM,    const.DELAY_EXECUTE_BNZ_AURICOM,
                    const.DELAY_EXECUTE_BZ_AURICOM,    const.DELAY_EXECUTE_B_AURICOM,
                    const.DELAY_EXECUTE_SWP_AURICOM,   const.DELAY_EXECUTE_ROL_AURICOM,
                    const.DELAY_EXECUTE_NOT_AURICOM,   const.DELAY_EXECUTE_XOR_AURICOM,
                    const.DELAY_EXECUTE_OR_AURICOM,    const.DELAY_EXECUTE_AND_AURICOM,
                    const.DELAY_EXECUTE_NEG_AURICOM,   const.DELAY_EXECUTE_ASR_AURICOM,
                    const.DELAY_EXECUTE_CMPI_AURICOM,  const.DELAY_EXECUTE_ADDI_AURICOM,
                    const.DELAY_EXECUTE_CMP_AURICOM,   const.DELAY_EXECUTE_SUB_AURICOM,
                    const.DELAY_EXECUTE_ADD_AURICOM ]
        Decode = [ const.DELAY_DECODE_CRASH_AURICOM, const.DELAY_DECODE_FORK_AURICOM,
                    const.DELAY_DECODE_MODE_AURICOM,  const.DELAY_DECODE_CHECK_AURICOM,
                    const.DELAY_DECODE_STAT_AURICOM,  const.DELAY_DECODE_WRITE_AURICOM,
                    const.DELAY_DECODE_STB_AURICOM,   const.DELAY_DECODE_LDB_AURICOM,
                    const.DELAY_DECODE_STR_AURICOM,   const.DELAY_DECODE_LDR_AURICOM,
                    const.DELAY_DECODE_LL_AURICOM,    const.DELAY_DECODE_LC_AURICOM,
                    const.DELAY_DECODE_MOV_AURICOM,   const.DELAY_DECODE_NOP_AURICOM,
                    const.DELAY_DECODE_BS_AURICOM,    const.DELAY_DECODE_BNZ_AURICOM,
                    const.DELAY_DECODE_BZ_AURICOM,    const.DELAY_DECODE_B_AURICOM,
                    const.DELAY_DECODE_SWP_AURICOM,   const.DELAY_DECODE_ROL_AURICOM,
                    const.DELAY_DECODE_NOT_AURICOM,   const.DELAY_DECODE_XOR_AURICOM,
                    const.DELAY_DECODE_OR_AURICOM,    const.DELAY_DECODE_AND_AURICOM,
                    const.DELAY_DECODE_NEG_AURICOM,   const.DELAY_DECODE_ASR_AURICOM,
                    const.DELAY_DECODE_CMPI_AURICOM,  const.DELAY_DECODE_ADDI_AURICOM,
                    const.DELAY_DECODE_CMP_AURICOM,   const.DELAY_DECODE_SUB_AURICOM,
                    const.DELAY_DECODE_ADD_AURICOM ]

    class Assegai:
        Name = "Assegai"
        Sight = const.IDX_MOD_ASSEGAI
        Execute = [ const.DELAY_EXECUTE_CRASH_ASSEGAI, const.DELAY_EXECUTE_FORK_ASSEGAI,
                    const.DELAY_EXECUTE_MODE_ASSEGAI,  const.DELAY_EXECUTE_CHECK_ASSEGAI,
                    const.DELAY_EXECUTE_STAT_ASSEGAI,  const.DELAY_EXECUTE_WRITE_ASSEGAI,
                    const.DELAY_EXECUTE_STB_ASSEGAI,   const.DELAY_EXECUTE_LDB_ASSEGAI,
                    const.DELAY_EXECUTE_STR_ASSEGAI,   const.DELAY_EXECUTE_LDR_ASSEGAI,
                    const.DELAY_EXECUTE_LL_ASSEGAI,    const.DELAY_EXECUTE_LC_ASSEGAI,
                    const.DELAY_EXECUTE_MOV_ASSEGAI,   const.DELAY_EXECUTE_NOP_ASSEGAI,
                    const.DELAY_EXECUTE_BS_ASSEGAI,    const.DELAY_EXECUTE_BNZ_ASSEGAI,
                    const.DELAY_EXECUTE_BZ_ASSEGAI,    const.DELAY_EXECUTE_B_ASSEGAI,
                    const.DELAY_EXECUTE_SWP_ASSEGAI,   const.DELAY_EXECUTE_ROL_ASSEGAI,
                    const.DELAY_EXECUTE_NOT_ASSEGAI,   const.DELAY_EXECUTE_XOR_ASSEGAI,
                    const.DELAY_EXECUTE_OR_ASSEGAI,    const.DELAY_EXECUTE_AND_ASSEGAI,
                    const.DELAY_EXECUTE_NEG_ASSEGAI,   const.DELAY_EXECUTE_ASR_ASSEGAI,
                    const.DELAY_EXECUTE_CMPI_ASSEGAI,  const.DELAY_EXECUTE_ADDI_ASSEGAI,
                    const.DELAY_EXECUTE_CMP_ASSEGAI,   const.DELAY_EXECUTE_SUB_ASSEGAI,
                    const.DELAY_EXECUTE_ADD_ASSEGAI ]
        Decode = [ const.DELAY_DECODE_CRASH_ASSEGAI, const.DELAY_DECODE_FORK_ASSEGAI,
                    const.DELAY_DECODE_MODE_ASSEGAI,  const.DELAY_DECODE_CHECK_ASSEGAI,
                    const.DELAY_DECODE_STAT_ASSEGAI,  const.DELAY_DECODE_WRITE_ASSEGAI,
                    const.DELAY_DECODE_STB_ASSEGAI,   const.DELAY_DECODE_LDB_ASSEGAI,
                    const.DELAY_DECODE_STR_ASSEGAI,   const.DELAY_DECODE_LDR_ASSEGAI,
                    const.DELAY_DECODE_LL_ASSEGAI,    const.DELAY_DECODE_LC_ASSEGAI,
                    const.DELAY_DECODE_MOV_ASSEGAI,   const.DELAY_DECODE_NOP_ASSEGAI,
                    const.DELAY_DECODE_BS_ASSEGAI,    const.DELAY_DECODE_BNZ_ASSEGAI,
                    const.DELAY_DECODE_BZ_ASSEGAI,    const.DELAY_DECODE_B_ASSEGAI,
                    const.DELAY_DECODE_SWP_ASSEGAI,   const.DELAY_DECODE_ROL_ASSEGAI,
                    const.DELAY_DECODE_NOT_ASSEGAI,   const.DELAY_DECODE_XOR_ASSEGAI,
                    const.DELAY_DECODE_OR_ASSEGAI,    const.DELAY_DECODE_AND_ASSEGAI,
                    const.DELAY_DECODE_NEG_ASSEGAI,   const.DELAY_DECODE_ASR_ASSEGAI,
                    const.DELAY_DECODE_CMPI_ASSEGAI,  const.DELAY_DECODE_ADDI_ASSEGAI,
                    const.DELAY_DECODE_CMP_ASSEGAI,   const.DELAY_DECODE_SUB_ASSEGAI,
                    const.DELAY_DECODE_ADD_ASSEGAI ]

    class Piranha:
        Name = "Piranha"
        Sight = const.IDX_MOD_PIRANHA
        Execute = [ const.DELAY_EXECUTE_CRASH_PIRANHA, const.DELAY_EXECUTE_FORK_PIRANHA,
                    const.DELAY_EXECUTE_MODE_PIRANHA,  const.DELAY_EXECUTE_CHECK_PIRANHA,
                    const.DELAY_EXECUTE_STAT_PIRANHA,  const.DELAY_EXECUTE_WRITE_PIRANHA,
                    const.DELAY_EXECUTE_STB_PIRANHA,   const.DELAY_EXECUTE_LDB_PIRANHA,
                    const.DELAY_EXECUTE_STR_PIRANHA,   const.DELAY_EXECUTE_LDR_PIRANHA,
                    const.DELAY_EXECUTE_LL_PIRANHA,    const.DELAY_EXECUTE_LC_PIRANHA,
                    const.DELAY_EXECUTE_MOV_PIRANHA,   const.DELAY_EXECUTE_NOP_PIRANHA,
                    const.DELAY_EXECUTE_BS_PIRANHA,    const.DELAY_EXECUTE_BNZ_PIRANHA,
                    const.DELAY_EXECUTE_BZ_PIRANHA,    const.DELAY_EXECUTE_B_PIRANHA,
                    const.DELAY_EXECUTE_SWP_PIRANHA,   const.DELAY_EXECUTE_ROL_PIRANHA,
                    const.DELAY_EXECUTE_NOT_PIRANHA,   const.DELAY_EXECUTE_XOR_PIRANHA,
                    const.DELAY_EXECUTE_OR_PIRANHA,    const.DELAY_EXECUTE_AND_PIRANHA,
                    const.DELAY_EXECUTE_NEG_PIRANHA,   const.DELAY_EXECUTE_ASR_PIRANHA,
                    const.DELAY_EXECUTE_CMPI_PIRANHA,  const.DELAY_EXECUTE_ADDI_PIRANHA,
                    const.DELAY_EXECUTE_CMP_PIRANHA,   const.DELAY_EXECUTE_SUB_PIRANHA,
                    const.DELAY_EXECUTE_ADD_PIRANHA ]
        Decode = [ const.DELAY_DECODE_CRASH_PIRANHA, const.DELAY_DECODE_FORK_PIRANHA,
                    const.DELAY_DECODE_MODE_PIRANHA,  const.DELAY_DECODE_CHECK_PIRANHA,
                    const.DELAY_DECODE_STAT_PIRANHA,  const.DELAY_DECODE_WRITE_PIRANHA,
                    const.DELAY_DECODE_STB_PIRANHA,   const.DELAY_DECODE_LDB_PIRANHA,
                    const.DELAY_DECODE_STR_PIRANHA,   const.DELAY_DECODE_LDR_PIRANHA,
                    const.DELAY_DECODE_LL_PIRANHA,    const.DELAY_DECODE_LC_PIRANHA,
                    const.DELAY_DECODE_MOV_PIRANHA,   const.DELAY_DECODE_NOP_PIRANHA,
                    const.DELAY_DECODE_BS_PIRANHA,    const.DELAY_DECODE_BNZ_PIRANHA,
                    const.DELAY_DECODE_BZ_PIRANHA,    const.DELAY_DECODE_B_PIRANHA,
                    const.DELAY_DECODE_SWP_PIRANHA,   const.DELAY_DECODE_ROL_PIRANHA,
                    const.DELAY_DECODE_NOT_PIRANHA,   const.DELAY_DECODE_XOR_PIRANHA,
                    const.DELAY_DECODE_OR_PIRANHA,    const.DELAY_DECODE_AND_PIRANHA,
                    const.DELAY_DECODE_NEG_PIRANHA,   const.DELAY_DECODE_ASR_PIRANHA,
                    const.DELAY_DECODE_CMPI_PIRANHA,  const.DELAY_DECODE_ADDI_PIRANHA,
                    const.DELAY_DECODE_CMP_PIRANHA,   const.DELAY_DECODE_SUB_PIRANHA,
                    const.DELAY_DECODE_ADD_PIRANHA ]

    class Qirex:
        Name = "Qirex"
        Sight = const.IDX_MOD_QIREX
        Execute = [ const.DELAY_EXECUTE_CRASH_QIREX, const.DELAY_EXECUTE_FORK_QIREX,
                    const.DELAY_EXECUTE_MODE_QIREX,  const.DELAY_EXECUTE_CHECK_QIREX,
                    const.DELAY_EXECUTE_STAT_QIREX,  const.DELAY_EXECUTE_WRITE_QIREX,
                    const.DELAY_EXECUTE_STB_QIREX,   const.DELAY_EXECUTE_LDB_QIREX,
                    const.DELAY_EXECUTE_STR_QIREX,   const.DELAY_EXECUTE_LDR_QIREX,
                    const.DELAY_EXECUTE_LL_QIREX,    const.DELAY_EXECUTE_LC_QIREX,
                    const.DELAY_EXECUTE_MOV_QIREX,   const.DELAY_EXECUTE_NOP_QIREX,
                    const.DELAY_EXECUTE_BS_QIREX,    const.DELAY_EXECUTE_BNZ_QIREX,
                    const.DELAY_EXECUTE_BZ_QIREX,    const.DELAY_EXECUTE_B_QIREX,
                    const.DELAY_EXECUTE_SWP_QIREX,   const.DELAY_EXECUTE_ROL_QIREX,
                    const.DELAY_EXECUTE_NOT_QIREX,   const.DELAY_EXECUTE_XOR_QIREX,
                    const.DELAY_EXECUTE_OR_QIREX,    const.DELAY_EXECUTE_AND_QIREX,
                    const.DELAY_EXECUTE_NEG_QIREX,   const.DELAY_EXECUTE_ASR_QIREX,
                    const.DELAY_EXECUTE_CMPI_QIREX,  const.DELAY_EXECUTE_ADDI_QIREX,
                    const.DELAY_EXECUTE_CMP_QIREX,   const.DELAY_EXECUTE_SUB_QIREX,
                    const.DELAY_EXECUTE_ADD_QIREX ]
        Decode = [ const.DELAY_DECODE_CRASH_QIREX, const.DELAY_DECODE_FORK_QIREX,
                    const.DELAY_DECODE_MODE_QIREX,  const.DELAY_DECODE_CHECK_QIREX,
                    const.DELAY_DECODE_STAT_QIREX,  const.DELAY_DECODE_WRITE_QIREX,
                    const.DELAY_DECODE_STB_QIREX,   const.DELAY_DECODE_LDB_QIREX,
                    const.DELAY_DECODE_STR_QIREX,   const.DELAY_DECODE_LDR_QIREX,
                    const.DELAY_DECODE_LL_QIREX,    const.DELAY_DECODE_LC_QIREX,
                    const.DELAY_DECODE_MOV_QIREX,   const.DELAY_DECODE_NOP_QIREX,
                    const.DELAY_DECODE_BS_QIREX,    const.DELAY_DECODE_BNZ_QIREX,
                    const.DELAY_DECODE_BZ_QIREX,    const.DELAY_DECODE_B_QIREX,
                    const.DELAY_DECODE_SWP_QIREX,   const.DELAY_DECODE_ROL_QIREX,
                    const.DELAY_DECODE_NOT_QIREX,   const.DELAY_DECODE_XOR_QIREX,
                    const.DELAY_DECODE_OR_QIREX,    const.DELAY_DECODE_AND_QIREX,
                    const.DELAY_DECODE_NEG_QIREX,   const.DELAY_DECODE_ASR_QIREX,
                    const.DELAY_DECODE_CMPI_QIREX,  const.DELAY_DECODE_ADDI_QIREX,
                    const.DELAY_DECODE_CMP_QIREX,   const.DELAY_DECODE_SUB_QIREX,
                    const.DELAY_DECODE_ADD_QIREX ]

    class Icaras:
        Name = "Icaras"
        Sight = const.IDX_MOD_ICARAS
        Execute = [ const.DELAY_EXECUTE_CRASH_ICARAS, const.DELAY_EXECUTE_FORK_ICARAS,
                    const.DELAY_EXECUTE_MODE_ICARAS,  const.DELAY_EXECUTE_CHECK_ICARAS,
                    const.DELAY_EXECUTE_STAT_ICARAS,  const.DELAY_EXECUTE_WRITE_ICARAS,
                    const.DELAY_EXECUTE_STB_ICARAS,   const.DELAY_EXECUTE_LDB_ICARAS,
                    const.DELAY_EXECUTE_STR_ICARAS,   const.DELAY_EXECUTE_LDR_ICARAS,
                    const.DELAY_EXECUTE_LL_ICARAS,    const.DELAY_EXECUTE_LC_ICARAS,
                    const.DELAY_EXECUTE_MOV_ICARAS,   const.DELAY_EXECUTE_NOP_ICARAS,
                    const.DELAY_EXECUTE_BS_ICARAS,    const.DELAY_EXECUTE_BNZ_ICARAS,
                    const.DELAY_EXECUTE_BZ_ICARAS,    const.DELAY_EXECUTE_B_ICARAS,
                    const.DELAY_EXECUTE_SWP_ICARAS,   const.DELAY_EXECUTE_ROL_ICARAS,
                    const.DELAY_EXECUTE_NOT_ICARAS,   const.DELAY_EXECUTE_XOR_ICARAS,
                    const.DELAY_EXECUTE_OR_ICARAS,    const.DELAY_EXECUTE_AND_ICARAS,
                    const.DELAY_EXECUTE_NEG_ICARAS,   const.DELAY_EXECUTE_ASR_ICARAS,
                    const.DELAY_EXECUTE_CMPI_ICARAS,  const.DELAY_EXECUTE_ADDI_ICARAS,
                    const.DELAY_EXECUTE_CMP_ICARAS,   const.DELAY_EXECUTE_SUB_ICARAS,
                    const.DELAY_EXECUTE_ADD_ICARAS ]
        Decode = [ const.DELAY_DECODE_CRASH_ICARAS, const.DELAY_DECODE_FORK_ICARAS,
                    const.DELAY_DECODE_MODE_ICARAS,  const.DELAY_DECODE_CHECK_ICARAS,
                    const.DELAY_DECODE_STAT_ICARAS,  const.DELAY_DECODE_WRITE_ICARAS,
                    const.DELAY_DECODE_STB_ICARAS,   const.DELAY_DECODE_LDB_ICARAS,
                    const.DELAY_DECODE_STR_ICARAS,   const.DELAY_DECODE_LDR_ICARAS,
                    const.DELAY_DECODE_LL_ICARAS,    const.DELAY_DECODE_LC_ICARAS,
                    const.DELAY_DECODE_MOV_ICARAS,   const.DELAY_DECODE_NOP_ICARAS,
                    const.DELAY_DECODE_BS_ICARAS,    const.DELAY_DECODE_BNZ_ICARAS,
                    const.DELAY_DECODE_BZ_ICARAS,    const.DELAY_DECODE_B_ICARAS,
                    const.DELAY_DECODE_SWP_ICARAS,   const.DELAY_DECODE_ROL_ICARAS,
                    const.DELAY_DECODE_NOT_ICARAS,   const.DELAY_DECODE_XOR_ICARAS,
                    const.DELAY_DECODE_OR_ICARAS,    const.DELAY_DECODE_AND_ICARAS,
                    const.DELAY_DECODE_NEG_ICARAS,   const.DELAY_DECODE_ASR_ICARAS,
                    const.DELAY_DECODE_CMPI_ICARAS,  const.DELAY_DECODE_ADDI_ICARAS,
                    const.DELAY_DECODE_CMP_ICARAS,   const.DELAY_DECODE_SUB_ICARAS,
                    const.DELAY_DECODE_ADD_ICARAS ]

    class Rocket:
        Name = "Rocket"
        Sight = const.IDX_MOD_ROCKET
        Execute = [ const.DELAY_EXECUTE_CRASH_ROCKET, const.DELAY_EXECUTE_FORK_ROCKET,
                    const.DELAY_EXECUTE_MODE_ROCKET,  const.DELAY_EXECUTE_CHECK_ROCKET,
                    const.DELAY_EXECUTE_STAT_ROCKET,  const.DELAY_EXECUTE_WRITE_ROCKET,
                    const.DELAY_EXECUTE_STB_ROCKET,   const.DELAY_EXECUTE_LDB_ROCKET,
                    const.DELAY_EXECUTE_STR_ROCKET,   const.DELAY_EXECUTE_LDR_ROCKET,
                    const.DELAY_EXECUTE_LL_ROCKET,    const.DELAY_EXECUTE_LC_ROCKET,
                    const.DELAY_EXECUTE_MOV_ROCKET,   const.DELAY_EXECUTE_NOP_ROCKET,
                    const.DELAY_EXECUTE_BS_ROCKET,    const.DELAY_EXECUTE_BNZ_ROCKET,
                    const.DELAY_EXECUTE_BZ_ROCKET,    const.DELAY_EXECUTE_B_ROCKET,
                    const.DELAY_EXECUTE_SWP_ROCKET,   const.DELAY_EXECUTE_ROL_ROCKET,
                    const.DELAY_EXECUTE_NOT_ROCKET,   const.DELAY_EXECUTE_XOR_ROCKET,
                    const.DELAY_EXECUTE_OR_ROCKET,    const.DELAY_EXECUTE_AND_ROCKET,
                    const.DELAY_EXECUTE_NEG_ROCKET,   const.DELAY_EXECUTE_ASR_ROCKET,
                    const.DELAY_EXECUTE_CMPI_ROCKET,  const.DELAY_EXECUTE_ADDI_ROCKET,
                    const.DELAY_EXECUTE_CMP_ROCKET,   const.DELAY_EXECUTE_SUB_ROCKET,
                    const.DELAY_EXECUTE_ADD_ROCKET ]
        Decode = [ const.DELAY_DECODE_CRASH_ROCKET, const.DELAY_DECODE_FORK_ROCKET,
                    const.DELAY_DECODE_MODE_ROCKET,  const.DELAY_DECODE_CHECK_ROCKET,
                    const.DELAY_DECODE_STAT_ROCKET,  const.DELAY_DECODE_WRITE_ROCKET,
                    const.DELAY_DECODE_STB_ROCKET,   const.DELAY_DECODE_LDB_ROCKET,
                    const.DELAY_DECODE_STR_ROCKET,   const.DELAY_DECODE_LDR_ROCKET,
                    const.DELAY_DECODE_LL_ROCKET,    const.DELAY_DECODE_LC_ROCKET,
                    const.DELAY_DECODE_MOV_ROCKET,   const.DELAY_DECODE_NOP_ROCKET,
                    const.DELAY_DECODE_BS_ROCKET,    const.DELAY_DECODE_BNZ_ROCKET,
                    const.DELAY_DECODE_BZ_ROCKET,    const.DELAY_DECODE_B_ROCKET,
                    const.DELAY_DECODE_SWP_ROCKET,   const.DELAY_DECODE_ROL_ROCKET,
                    const.DELAY_DECODE_NOT_ROCKET,   const.DELAY_DECODE_XOR_ROCKET,
                    const.DELAY_DECODE_OR_ROCKET,    const.DELAY_DECODE_AND_ROCKET,
                    const.DELAY_DECODE_NEG_ROCKET,   const.DELAY_DECODE_ASR_ROCKET,
                    const.DELAY_DECODE_CMPI_ROCKET,  const.DELAY_DECODE_ADDI_ROCKET,
                    const.DELAY_DECODE_CMP_ROCKET,   const.DELAY_DECODE_SUB_ROCKET,
                    const.DELAY_DECODE_ADD_ROCKET ]

    class Missile:
        Name = "Missile"
        Sight = const.IDX_MOD_MISSILE
        Execute = [ const.DELAY_EXECUTE_CRASH_MISSILE, const.DELAY_EXECUTE_FORK_MISSILE,
                    const.DELAY_EXECUTE_MODE_MISSILE,  const.DELAY_EXECUTE_CHECK_MISSILE,
                    const.DELAY_EXECUTE_STAT_MISSILE,  const.DELAY_EXECUTE_WRITE_MISSILE,
                    const.DELAY_EXECUTE_STB_MISSILE,   const.DELAY_EXECUTE_LDB_MISSILE,
                    const.DELAY_EXECUTE_STR_MISSILE,   const.DELAY_EXECUTE_LDR_MISSILE,
                    const.DELAY_EXECUTE_LL_MISSILE,    const.DELAY_EXECUTE_LC_MISSILE,
                    const.DELAY_EXECUTE_MOV_MISSILE,   const.DELAY_EXECUTE_NOP_MISSILE,
                    const.DELAY_EXECUTE_BS_MISSILE,    const.DELAY_EXECUTE_BNZ_MISSILE,
                    const.DELAY_EXECUTE_BZ_MISSILE,    const.DELAY_EXECUTE_B_MISSILE,
                    const.DELAY_EXECUTE_SWP_MISSILE,   const.DELAY_EXECUTE_ROL_MISSILE,
                    const.DELAY_EXECUTE_NOT_MISSILE,   const.DELAY_EXECUTE_XOR_MISSILE,
                    const.DELAY_EXECUTE_OR_MISSILE,    const.DELAY_EXECUTE_AND_MISSILE,
                    const.DELAY_EXECUTE_NEG_MISSILE,   const.DELAY_EXECUTE_ASR_MISSILE,
                    const.DELAY_EXECUTE_CMPI_MISSILE,  const.DELAY_EXECUTE_ADDI_MISSILE,
                    const.DELAY_EXECUTE_CMP_MISSILE,   const.DELAY_EXECUTE_SUB_MISSILE,
                    const.DELAY_EXECUTE_ADD_MISSILE ]
        Decode = [ const.DELAY_DECODE_CRASH_MISSILE, const.DELAY_DECODE_FORK_MISSILE,
                    const.DELAY_DECODE_MODE_MISSILE,  const.DELAY_DECODE_CHECK_MISSILE,
                    const.DELAY_DECODE_STAT_MISSILE,  const.DELAY_DECODE_WRITE_MISSILE,
                    const.DELAY_DECODE_STB_MISSILE,   const.DELAY_DECODE_LDB_MISSILE,
                    const.DELAY_DECODE_STR_MISSILE,   const.DELAY_DECODE_LDR_MISSILE,
                    const.DELAY_DECODE_LL_MISSILE,    const.DELAY_DECODE_LC_MISSILE,
                    const.DELAY_DECODE_MOV_MISSILE,   const.DELAY_DECODE_NOP_MISSILE,
                    const.DELAY_DECODE_BS_MISSILE,    const.DELAY_DECODE_BNZ_MISSILE,
                    const.DELAY_DECODE_BZ_MISSILE,    const.DELAY_DECODE_B_MISSILE,
                    const.DELAY_DECODE_SWP_MISSILE,   const.DELAY_DECODE_ROL_MISSILE,
                    const.DELAY_DECODE_NOT_MISSILE,   const.DELAY_DECODE_XOR_MISSILE,
                    const.DELAY_DECODE_OR_MISSILE,    const.DELAY_DECODE_AND_MISSILE,
                    const.DELAY_DECODE_NEG_MISSILE,   const.DELAY_DECODE_ASR_MISSILE,
                    const.DELAY_DECODE_CMPI_MISSILE,  const.DELAY_DECODE_ADDI_MISSILE,
                    const.DELAY_DECODE_CMP_MISSILE,   const.DELAY_DECODE_SUB_MISSILE,
                    const.DELAY_DECODE_ADD_MISSILE ]

    class Mine:
        Name = "Mine"
        Sight = const.IDX_MOD_MINE
        Execute = [ const.DELAY_EXECUTE_CRASH_MINE, const.DELAY_EXECUTE_FORK_MINE,
                    const.DELAY_EXECUTE_MODE_MINE,  const.DELAY_EXECUTE_CHECK_MINE,
                    const.DELAY_EXECUTE_STAT_MINE,  const.DELAY_EXECUTE_WRITE_MINE,
                    const.DELAY_EXECUTE_STB_MINE,   const.DELAY_EXECUTE_LDB_MINE,
                    const.DELAY_EXECUTE_STR_MINE,   const.DELAY_EXECUTE_LDR_MINE,
                    const.DELAY_EXECUTE_LL_MINE,    const.DELAY_EXECUTE_LC_MINE,
                    const.DELAY_EXECUTE_MOV_MINE,   const.DELAY_EXECUTE_NOP_MINE,
                    const.DELAY_EXECUTE_BS_MINE,    const.DELAY_EXECUTE_BNZ_MINE,
                    const.DELAY_EXECUTE_BZ_MINE,    const.DELAY_EXECUTE_B_MINE,
                    const.DELAY_EXECUTE_SWP_MINE,   const.DELAY_EXECUTE_ROL_MINE,
                    const.DELAY_EXECUTE_NOT_MINE,   const.DELAY_EXECUTE_XOR_MINE,
                    const.DELAY_EXECUTE_OR_MINE,    const.DELAY_EXECUTE_AND_MINE,
                    const.DELAY_EXECUTE_NEG_MINE,   const.DELAY_EXECUTE_ASR_MINE,
                    const.DELAY_EXECUTE_CMPI_MINE,  const.DELAY_EXECUTE_ADDI_MINE,
                    const.DELAY_EXECUTE_CMP_MINE,   const.DELAY_EXECUTE_SUB_MINE,
                    const.DELAY_EXECUTE_ADD_MINE ]
        Decode = [ const.DELAY_DECODE_CRASH_MINE, const.DELAY_DECODE_FORK_MINE,
                    const.DELAY_DECODE_MODE_MINE,  const.DELAY_DECODE_CHECK_MINE,
                    const.DELAY_DECODE_STAT_MINE,  const.DELAY_DECODE_WRITE_MINE,
                    const.DELAY_DECODE_STB_MINE,   const.DELAY_DECODE_LDB_MINE,
                    const.DELAY_DECODE_STR_MINE,   const.DELAY_DECODE_LDR_MINE,
                    const.DELAY_DECODE_LL_MINE,    const.DELAY_DECODE_LC_MINE,
                    const.DELAY_DECODE_MOV_MINE,   const.DELAY_DECODE_NOP_MINE,
                    const.DELAY_DECODE_BS_MINE,    const.DELAY_DECODE_BNZ_MINE,
                    const.DELAY_DECODE_BZ_MINE,    const.DELAY_DECODE_B_MINE,
                    const.DELAY_DECODE_SWP_MINE,   const.DELAY_DECODE_ROL_MINE,
                    const.DELAY_DECODE_NOT_MINE,   const.DELAY_DECODE_XOR_MINE,
                    const.DELAY_DECODE_OR_MINE,    const.DELAY_DECODE_AND_MINE,
                    const.DELAY_DECODE_NEG_MINE,   const.DELAY_DECODE_ASR_MINE,
                    const.DELAY_DECODE_CMPI_MINE,  const.DELAY_DECODE_ADDI_MINE,
                    const.DELAY_DECODE_CMP_MINE,   const.DELAY_DECODE_SUB_MINE,
                    const.DELAY_DECODE_ADD_MINE ]

    class Plasma:
        Name = "Plasma"
        Sight = const.IDX_MOD_PLASMA
        Execute = [ const.DELAY_EXECUTE_CRASH_PLASMA, const.DELAY_EXECUTE_FORK_PLASMA,
                    const.DELAY_EXECUTE_MODE_PLASMA,  const.DELAY_EXECUTE_CHECK_PLASMA,
                    const.DELAY_EXECUTE_STAT_PLASMA,  const.DELAY_EXECUTE_WRITE_PLASMA,
                    const.DELAY_EXECUTE_STB_PLASMA,   const.DELAY_EXECUTE_LDB_PLASMA,
                    const.DELAY_EXECUTE_STR_PLASMA,   const.DELAY_EXECUTE_LDR_PLASMA,
                    const.DELAY_EXECUTE_LL_PLASMA,    const.DELAY_EXECUTE_LC_PLASMA,
                    const.DELAY_EXECUTE_MOV_PLASMA,   const.DELAY_EXECUTE_NOP_PLASMA,
                    const.DELAY_EXECUTE_BS_PLASMA,    const.DELAY_EXECUTE_BNZ_PLASMA,
                    const.DELAY_EXECUTE_BZ_PLASMA,    const.DELAY_EXECUTE_B_PLASMA,
                    const.DELAY_EXECUTE_SWP_PLASMA,   const.DELAY_EXECUTE_ROL_PLASMA,
                    const.DELAY_EXECUTE_NOT_PLASMA,   const.DELAY_EXECUTE_XOR_PLASMA,
                    const.DELAY_EXECUTE_OR_PLASMA,    const.DELAY_EXECUTE_AND_PLASMA,
                    const.DELAY_EXECUTE_NEG_PLASMA,   const.DELAY_EXECUTE_ASR_PLASMA,
                    const.DELAY_EXECUTE_CMPI_PLASMA,  const.DELAY_EXECUTE_ADDI_PLASMA,
                    const.DELAY_EXECUTE_CMP_PLASMA,   const.DELAY_EXECUTE_SUB_PLASMA,
                    const.DELAY_EXECUTE_ADD_PLASMA ]
        Decode = [ const.DELAY_DECODE_CRASH_PLASMA, const.DELAY_DECODE_FORK_PLASMA,
                    const.DELAY_DECODE_MODE_PLASMA,  const.DELAY_DECODE_CHECK_PLASMA,
                    const.DELAY_DECODE_STAT_PLASMA,  const.DELAY_DECODE_WRITE_PLASMA,
                    const.DELAY_DECODE_STB_PLASMA,   const.DELAY_DECODE_LDB_PLASMA,
                    const.DELAY_DECODE_STR_PLASMA,   const.DELAY_DECODE_LDR_PLASMA,
                    const.DELAY_DECODE_LL_PLASMA,    const.DELAY_DECODE_LC_PLASMA,
                    const.DELAY_DECODE_MOV_PLASMA,   const.DELAY_DECODE_NOP_PLASMA,
                    const.DELAY_DECODE_BS_PLASMA,    const.DELAY_DECODE_BNZ_PLASMA,
                    const.DELAY_DECODE_BZ_PLASMA,    const.DELAY_DECODE_B_PLASMA,
                    const.DELAY_DECODE_SWP_PLASMA,   const.DELAY_DECODE_ROL_PLASMA,
                    const.DELAY_DECODE_NOT_PLASMA,   const.DELAY_DECODE_XOR_PLASMA,
                    const.DELAY_DECODE_OR_PLASMA,    const.DELAY_DECODE_AND_PLASMA,
                    const.DELAY_DECODE_NEG_PLASMA,   const.DELAY_DECODE_ASR_PLASMA,
                    const.DELAY_DECODE_CMPI_PLASMA,  const.DELAY_DECODE_ADDI_PLASMA,
                    const.DELAY_DECODE_CMP_PLASMA,   const.DELAY_DECODE_SUB_PLASMA,
                    const.DELAY_DECODE_ADD_PLASMA ]














