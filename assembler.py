from custom_types import LineType
import instructions
import helpers
import dicts
import re

# Dictionary mapping labels to their corresponding byte addresses
symbol_table = {}

# Dictionary mapping variables to their byte addresses
# (points to start of data if multiple bytes)
variable_table = {}

# List containing the type of each line in the assembly file
# possible types are given in the LineType enum
# indexed by line number starting with 0 as first line
line_type_list = []

# Random byte memory address where the first instruction will be placed in memory
# Can be changed to anything, but note that it should be word aligned since
# each instruction occupies 1 word
START_ADDRESS = 7996


# TODO remove o_file when no longer testing
def process_first_pass(i_file, o_file):
    """
    Scans through the file line by line searching for symbols (labels, variables etc.)
    and adds them to the symbol table
    :param i_file: assembly language input file handle (previously opened and ready to read from)
    :return: None
    :raises Exception if a line is invalid
    """
    # Initialize current instruction address counter variable (in bytes, each instruction is 4 bytes)
    # (less 4 because it will be incremented upon reaching the first valid instruction)
    current_instruction_address = START_ADDRESS-4
    i_file.seek(0)  # Reset read pointer to top of file
    for line_number, line in enumerate(i_file):

        # Determine line type and fill out line_type_table
        line_type = helpers.get_line_type(line)
        line_type_list.append(line_type)

        # TODO remove Temp
        o_file.write("{} {}     {}".format(line_number, line_type, line))

        # Catch and report invalid lines at this stage
        if line_type == LineType.INVALID:
            raise Exception("Error invalid line encountered in assembly file\n"
                            "Line number: ", line_number+1, "\n",               # +1 since first line is 0
                            "Line: ", line)

        # Increment current instruction address if valid instruction
        if line_type in [LineType.R_INSTRUCTION, LineType.I_INSTRUCTION, LineType.J_INSTRUCTION,
                         LineType.LABEL_WITH_R_INSTR, LineType.LABEL_WITH_I_INSTR, LineType.LABEL_WITH_J_INSTR]:
            # Increment instruction address counter by 4 bytes (since each instruction is 1 word)
            current_instruction_address += 4

        # Fill out variable table
        if line_type == LineType.VARIABLE:
            variable = re.search(dicts.REGEX_DICT["variable"], line)
            # TODO

        # Fill out symbol/label table
        if line_type in [LineType.LABEL_ONLY, LineType.LABEL_WITH_U_INSTR, LineType.LABEL_WITH_R_INSTR,
                         LineType.LABEL_WITH_I_INSTR, LineType.LABEL_WITH_J_INSTR]:
            # Isolate label portion (remove the instruction or comment portions) and strip whitespace
            label = line.split(":", 1)[0].strip()  # Split on the ":", max of 1 split, keep the first portion

            # Add label and its associated instruction address to symbol table
            if line_type == LineType.LABEL_ONLY:
                # Since it is a label only, the associated instruction is the next instruction, so add 4 bytes
                symbol_table[label] = current_instruction_address + 4
            else:
                # Since it is a label with an instruction, the associated instruction is on the same line, so no offset
                symbol_table[label] = current_instruction_address
    return


def process_second_pass(i_file, o_file):
    # TODO
    pass


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
                    # Begin assembly process
                    try:
                        # Perform first pass (build symbol table etc.)
                        process_first_pass(i_file, o_file)

                        # Perform second pass (assemble file)
                        process_second_pass(i_file, o_file)
                    except Exception as error:
                        print(error)
    return


def assemble_instruction(instr_line_list: list):
    # TODO probably split this into 3 different functions: assemble, R, J, and I
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

    return
