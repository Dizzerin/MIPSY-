import dicts
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


def assemble_instruction(instr_line_list: list):
    instr_dict = None

    # Get mnemonic portion
    mnemonic = instr_line_list[0]
    # Check if mnemonic matches a valid instruction
    if mnemonic in instructions.instruction_list:
        instr_dict = instructions.instruction_list[mnemonic]
    # else check if it is technically an instruction, but not yet supported
    elif mnemonic in instructions.unsupported_instruction_list:
        print("Unsupported Instruction: {}".format(mnemonic))
    else:
        raise Exception("Invalid Instruction")

    # If valid instruction...
    if instr_dict is not None:
        # Aliases
        instr_type = instr_dict.get("type")
        instr_opcode = instr_dict.get("opcode")
        instr_funct = instr_dict.get("funct")
        instr_format = instr_dict.get("format")
        # Check if it matches the expected format
        if instr_type == "R":
            # Number of fields in instruction line list should equal len(format list)+1
            if len(instr_line_list) != len(instr_format)+1:
                print("Error, instruction did not match expected format.")
                return
            else:
                # Instruction contains the right number of fields, make sure each field is valid
                for i, expctd_format in enumerate(instr_format):
                    """
                    Format options are:
                        - "rs"
                        - "rt"
                        - "rd"
                        - "imm"
                        - "label"
                        - "imm(rs)"
                        - "shamt"
                    """
                    # make sure instr_line_list[i+1] is type specified by format
                    instr_param = instr_line_list[i+1]
                    if expctd_format in ["rs", "rt", "rd"]:
                        if instr_param not in dicts.REGISTER_DICT:
                            print("Error, invalid register specified")
                            return
                        else:
                            #TODO
                            pass
                    elif expctd_format == "imm":
                        pass
                    elif expctd_format == "label":
                        pass
                    elif expctd_format == "imm(rs)":
                        pass
                    elif expctd_format == "shamt":
                        pass
                    else:
                        # Should never get here
                        raise Exception("Invalid format in format list")

        elif instr_type == "I":
            pass
        elif instr_type == "J":
            pass
        else:
            # Should never get here
            raise Exception("Unknown instruction type specified in instruction list")
    else:
        print("Invalid Instruction")


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
        instruction_line = instruction_line.split("#")[0]
        # Split on any whitespace (and discard the whitespace)
        instruction_line_list = instruction_line.split()
        # TODO change below
        assemble_instruction(instruction_line_list)

        # else:
        # print("Invalid instruction encountered!")
        # print("Line number: ", line_number)
        # print("Line: ", line)
        # line_type = LineType.INVALID

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
