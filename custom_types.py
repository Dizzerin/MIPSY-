from enum import Enum


# Types of lines that can be found in an assembly file
class LineType(Enum):
    BLANK = 0
    COMMENT = 1
    ASSM_DIRECTIVE = 2          # Assembler directive
    LABEL_ONLY = 3              # Label on a line by itself
    LABEL_WITH_R_INSTR = 4      # Label on same line as an R type instruction
    LABEL_WITH_I_INSTR = 5      # Label on same line as an I type instruction
    LABEL_WITH_J_INSTR = 6      # Label on same line as a J type instruction
    LABEL_WITH_U_INSTR = 7      # Label on same line as a U type instruction (valid but unsupported type)
    VARIABLE = 8
    R_INSTRUCTION = 9
    I_INSTRUCTION = 10
    J_INSTRUCTION = 11
    U_INSTRUCTION = 12          # Used for instructions that are in MIPS, but not supported by this assembler
    INVALID_INSTRUCTION = 13    # Looks like an instruction, but is invalid
    INVALID = 14


ALL_INSTRUCTIONAL_TYPES = [LineType.R_INSTRUCTION, LineType.I_INSTRUCTION, LineType.J_INSTRUCTION,
                           LineType.LABEL_WITH_R_INSTR, LineType.LABEL_WITH_I_INSTR, LineType.LABEL_WITH_J_INSTR]

ALL_LABEL_TYPES = [LineType.LABEL_ONLY, LineType.LABEL_WITH_U_INSTR, LineType.LABEL_WITH_R_INSTR,
                   LineType.LABEL_WITH_I_INSTR, LineType.LABEL_WITH_J_INSTR]

ALL_INSTRUCTIONAL_LABEL_TYPES = [LineType.LABEL_WITH_U_INSTR, LineType.LABEL_WITH_R_INSTR,
                                 LineType.LABEL_WITH_I_INSTR, LineType.LABEL_WITH_J_INSTR]

ALL_INSTRUCTION_ONLY_TYPES = [LineType.R_INSTRUCTION, LineType.I_INSTRUCTION, LineType.J_INSTRUCTION]