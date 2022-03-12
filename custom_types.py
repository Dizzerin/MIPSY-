from enum import Enum


class LineType(Enum):
    BLANK = 0
    COMMENT = 1
    ASSM_DIRECTIVE = 2
    LABEL_ONLY = 3
    LABEL_WITH_INSTR = 4
    VARIABLE = 5
    R_INSTRUCTION = 6
    I_INSTRUCTION = 7
    J_INSTRUCTION = 8
    INVALID = 9
