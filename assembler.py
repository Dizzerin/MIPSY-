import helpers
import re

import instructions


def assemble(assembly_filename, assembled_filename):
    # Open input file
    with helpers.open_with_error(assembly_filename, "r") as (i_file, i_error):
        # Check for error opening input file
        if i_error:
            print("Error occurred opening input file.")
            print("Error: ", i_error)
        else:

            # Create output file
            # TODO change mode to "x" to prevent overwriting files
            with helpers.open_with_error(assembled_filename, "w") as (o_file, o_error):
                # Check for error creating output file
                if o_error:
                    print("Error occurred creating output file.")
                    print("Error: ", o_error)
                else:

                    # Scan file once, get labels
                    for line_number, line in enumerate(i_file):
                        o_file.write(str(get_line_type(line, line_number)) + "\t\t" + str(line))

                    # Scan file again, assemble
                    # i_file.seek(0)  # Reset read pointer to top of file
                    # for line in i_file:
                    #     print(line, end="")


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


def get_line_type(line, line_number):
    """
    Parses and tokenizes each line
    :param line: assembly file line
    :param line_number: line number
    :return:
    """
    """
    Line Type Options
        - blank
        - comment
        - assembler directive
        - label
            - label only
            - label and instruction
            - variable
        - instruction
        - invalid line
    """
    line_type = LineType.INVALID

    if line.strip() == "":
        line_type = LineType.BLANK

    # if first non-whitespace char is "#" it's a comment
    elif re.search(r"^\s*#.*", line):
        line_type = LineType.COMMENT

    # Line below matches any line that starts like an instruction
    # The full validity of the instruction has yet to be verified
    elif re.search(r"^\s*[a-zA-Z]+(\s+[a-zA-Z]+\w*|(\s+\$.*)+).*", line):
        instruction_line = re.search(r"^\s*[a-zA-Z]+(\s+[a-zA-Z]+\w*|(\s+\$.*)+).*", line).group(0)
        # Split off and discard any comment portion
        instruction_line_list = instruction_line.split("#")[0]
        # Split on any whitespace (and discard the whitespace)
        instruction_line_list = instruction_line.split()
        # Get mnemonic portion
        mnemonic = instruction_line_list[0]
        # Check if mnemonic matches a valid instruction
        if mnemonic in instructions.instructions_list:
            instr_format = instructions.instructions_list[mnemonic]["format"]

            if instr_format == "R":
                line_type = LineType.R_INSTRUCTION
            elif instr_format == "I":
                line_type = LineType.I_INSTRUCTION
            elif instr_format == "J":
                line_type = LineType.J_INSTRUCTION
            else:
                # Should never get here
                raise Exception("format for instruction in instruction list not valid")

        else:
            print("Invalid instruction encountered!")
            print("Line number: ", line_number)
            print("Line: ", line)
            line_type = LineType.INVALID

    # if it matches the regex pattern below it's a label only
    elif re.search(r"^\s*[a-zA-Z]+\w*:\s*$", line):
        line_type = LineType.LABEL_ONLY

    # if it matches the regex pattern below it's a variable
    elif re.search(r"^\s*[a-zA-Z]+\w*:\s+\.[a-zA-Z]\w*\s+\d+", line):
        line_type = LineType.VARIABLE

    # if it matches the regex pattern below it is a label most likely followed by an instruction
    # however the validity of the instruction portion has yet to be verified
    elif re.search(r"^\s*[a-zA-Z]+\w*:\s+[a-zA-Z]+\s+[a-zA-Z$]", line):
        line_type = LineType.LABEL_WITH_INSTR

    # if first non-whitespace char is "." and it's followed by an any number of alphanumeric characters it's an assembler directive
    elif re.search(r"^\s*\.\w+", line):
        line_type = LineType.ASSM_DIRECTIVE

    else:
        print("Error invalid line type encountered")
        print("Line number: ", line_number)
        print("Line: ", line)
        line_type = LineType.INVALID

    return line_type
