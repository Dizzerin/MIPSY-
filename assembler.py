import custom_types
from custom_types import LineType
from instruction_assemblers import *
import helpers
import dicts
import re

# Random byte memory address where the first instruction will be placed in memory
# Can be changed to anything, but note that it should be word aligned since
# each instruction occupies 1 word
START_ADDRESS = 7996


# TODO remove o_file when no longer testing
def process_first_pass(i_file, o_file):
    """
    Scans through the file line by line
    determines each line's type and saves it to the respective index in the line_type_list,
    if the line contains a symbol/label, it will add it to the symbol table with its proper address
    TODO: also add variables to the variable table
    :param i_file: assembly language input file handle (previously opened and ready to read from)
    :return: Tuple (symbol table, variable table, line type list)
    :raises Exception if a line is invalid
    """
    # Dictionary mapping labels to their corresponding byte addresses
    symbol_table = {}

    # Dictionary mapping variables to their byte addresses
    # (points to start of data if multiple bytes)
    variable_table = {}

    # List containing the type of each line in the assembly file
    # possible types are given in the LineType enum
    # indexed by line number starting with 0 as first line
    line_type_list = []

    # Initialize current instruction address counter variable (in bytes, each instruction is 4 bytes)
    # (less 4 because it will be incremented upon reaching the first valid instruction)
    current_instruction_address = START_ADDRESS-4
    i_file.seek(0)  # Reset read pointer to top of file
    for line_number, line in enumerate(i_file):

        # Determine line type and fill out line_type_list
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
        if line_type in custom_types.ALL_INSTRUCTIONAL_TYPES:
            # Increment instruction address counter by 4 bytes (since each instruction is 1 word)
            current_instruction_address += 4

        # Fill out variable table
        if line_type == LineType.VARIABLE:
            variable = re.search(dicts.REGEX_DICT["variable"], line)
            # TODO fill out variable table (support variables)

        # Fill out symbol/label table
        if line_type in custom_types.ALL_LABEL_TYPES:
            # Isolate label portion (remove the instruction or comment portions) and strip whitespace
            label = line.split(":", 1)[0].strip()  # Split on the ":", max of 1 split, keep the first portion

            # Add label and its associated instruction address to symbol table
            if line_type == LineType.LABEL_ONLY:
                # Since it is a label only, the associated instruction is the next instruction, so add 4 bytes
                symbol_table[label] = current_instruction_address + 4
            else:
                # Since it is a label with an instruction, the associated instruction is on the same line, so no offset
                symbol_table[label] = current_instruction_address

    return symbol_table, variable_table, line_type_list


def process_second_pass(i_file, o_file, symbol_table, variable_table, line_type_list):
    # Read through line_type_list and only operate on lines that contain instructions
    for line_number, line_type in enumerate(line_type_list):
        # For every instruction line...
        if line_type in custom_types.ALL_INSTRUCTIONAL_TYPES:
            # Goto that line in the input file
            i_file.seek(line_number)
            # Grab the line from the file
            line = i_file.readline()
            # Set a flag indicating if the instruction starts with a label on the same line
            with_label = line_type in custom_types.ALL_INSTRUCTIONAL_LABEL_TYPES
            # Tokenize instruction
            tokenized_instr_list = tokenize_instruction(line, with_label)
            # Verify instruction
            verify_instruction_tokens(tokenized_instr_list, symbol_table)
            # Assemble instruction
            # TODO call appropriate assembler (R type, I type.. etc.)

            # Write to output file(s)


def assemble(assembly_filename, assembled_filename):
    """
    This function is primarily responsible for the file handling aspects surrounding the assembly process.
    It verifies the input file can be read and output file can be written to etc.
    opens the input file and creates and opens the output file with error handling
    and then passes the opened and validated file handles to the first pass and second pass functions
    It also catches the exceptions that may occur during the assembly process and prints them
    :param assembly_filename: input filename (or full path if not in the same directory) (include file extension)
    :param assembled_filename: output filename (or full path if not in the same directory) (don't include extension)
    :return: None
    """
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
                        # Perform first pass (build symbol table, determine line types, etc.)
                        symbol_table, variable_table, line_type_list = process_first_pass(i_file, o_file)

                        # Perform second pass (assemble file)
                        process_second_pass(i_file, o_file, symbol_table, variable_table, line_type_list)
                    except Exception as error:
                        print(error)
    return

