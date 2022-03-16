from contextlib import contextmanager
from custom_types import LineType
import instructions
import dicts
import re


@contextmanager
def open_with_error(filename, mode="r"):
    """
    Custom function which can be used in a with statement
    in place of the open function.  The advantage of using
    this function is it catches errors.  This opener
    ensures the file handle is properly closed at the end.
    """
    try:
        f = open(filename, mode)
    except IOError as error:
        yield None, error
    else:
        try:
            yield f, None
        finally:
            f.close()


def get_line_type(line):
    """
    determines the type of the provided line
    :param line: assembly file line
    :return: LineType (see LineType enum for options)
    :rtype: LineType
    """
    if line.strip() == "":
        return LineType.BLANK

    # If first non-whitespace char is "#" it's a comment
    if re.search(dicts.REGEX_DICT["comment"], line):
        return LineType.COMMENT

    # If it matches the regex pattern below it's a label only
    if re.search(dicts.REGEX_DICT["label_only"], line):
        return LineType.LABEL_ONLY

    # If it matches the regex pattern below it's a variable
    if re.search(dicts.REGEX_DICT["variable"], line):
        return LineType.VARIABLE

    # If it matches the regex pattern below it is a label most likely followed by an instruction
    # however the validity of the instruction portion has yet to be verified
    if re.search(dicts.REGEX_DICT["label_and_instr"], line):
        return get_instruction_type(line)

    # Line below matches any line that starts like an instruction
    # The full validity of the instruction has yet to be verified
    if re.search(dicts.REGEX_DICT["instruction"], line):
        return get_instruction_type(line)

    # If it matches the regex pattern below it's an assembler directive
    if re.search(dicts.REGEX_DICT["directive"], line):
        return LineType.ASSM_DIRECTIVE

    # Else it's an invalid line
    return LineType.INVALID


def get_instruction_type(instruction_line):
    """
    Determines the type of instruction
    Performs basic instruction verification
        Only checks the mnemonic to see if it is a supported instruction, doesn't check anything beyond the mnemonic
    :param instruction_line: line containing instruction from assembly file (string)
    :return: Returns the instruction type (see LineType enum)
    :rtype: LineType (or None) if the line doesn't match an instruction format
    """
    with_label = False              # Boolean indicating if the line contains a label along with the instruction
    instruction = instruction_line

    # Make sure the line follows a general instruction format (either with or without label)
    # If the line starts with a label....
    if re.search(dicts.REGEX_DICT["label_and_instr"], instruction_line):
        with_label = True
        # Remove the label portion
        instruction = instruction.split(":", 1)[1]  # Split on the ":", max of 1 split, keep the second portion

    # else, make sure it is still likely an instruction of some sort
    elif not re.search(dicts.REGEX_DICT["instruction"], instruction_line):
        return None

    # Now check to see if the instruction is supported and determine type if so
    """
    Note: only the mnemonic portion is checked, the validity of the rest of the instruction
    (i.e. providing the right number of arguments/registers, labels, trying to modify
    protected/reserved registers etc. is not checked at this stage).
    Instructions that are deemed valid at this stage will have the above things checked by the assembler
    during the second pass.
    """
    # Split off and discard any trailing comment portion
    instruction = instruction.split("#", 1)[0]
    # Split on any whitespace (and discard the whitespace, no need for additional trimming)
    instr_line_list = instruction.split()
    # Get mnemonic portion
    mnemonic = instr_line_list[0]
    # Check if mnemonic matches a valid instruction
    if mnemonic in instructions.instruction_list:
        instr_type_dict = instructions.instruction_list[mnemonic]
        # Get type of instruction
        if instr_type_dict["type"] == "R":
            return LineType.R_INSTRUCTION if with_label is False else LineType.LABEL_WITH_R_INSTR
        if instr_type_dict["type"] == "I":
            return LineType.I_INSTRUCTION if with_label is False else LineType.LABEL_WITH_I_INSTR
        if instr_type_dict["type"] == "J":
            return LineType.J_INSTRUCTION if with_label is False else LineType.LABEL_WITH_J_INSTR

    # else check if it is technically an instruction, but not yet supported
    elif mnemonic in instructions.unsupported_instruction_list:
        return LineType.U_INSTRUCTION if with_label is False else LineType.LABEL_WITH_U_INSTR

    return LineType.INVALID_INSTRUCTION
