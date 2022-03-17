from custom_types import LineType
import instructions
from helpers import sign_extend
import dicts
import re


def tokenize_instruction(line, with_label):
    """
    This function isolates the instruction, removes whitespace, commas, etc., breaks the instruction up into a list
    of tokens and returns that list
    Note: This function should only be called once a line is known to start with a valid and supported instruction
    mnemonic.

    :param line: line of text containing the instruction and possible trailing comments (string)
    :param with_label: boolean indicating if the line starts with a label (as opposed to a standalone instruction)
    :return: tokenized_instr_list (list)
    """
    instruction = line

    # If the line starts with a label....
    if with_label:
        # Remove the label portion
        instruction = instruction.split(":", 1)[1]  # Split on the ":", max of 1 split, keep the second portion

    # Split off and discard any trailing comment portion
    instruction = instruction.split("#", 1)[0]
    # Remove any commas
    instruction = instruction.replace(",", "")
    # Split on any whitespace (and discard the whitespace, no need for additional trimming)
    tokenized_instr_list = instruction.split()

    return tokenized_instr_list


def verify_instruction_tokens(tokenized_instr_list, symbol_table):
    """
    This function uses the instruction mnemonic to find the proper instr_format_dict in the instruction_list
    It then performs some basic verification checks on the instruction such as:
        Verifying expected number of tokens
        Verifying provided registers are valid
        Verifying provided immediate values are numeric and within range
        Verifying provided shift amounts are numeric and within range
        etc. (see function for full list)
    If any of those verifications fail, it raises an exception
    If they all pass, this function will return the instr_format_dict which contains the expected format info for the
        provided instruction mnemonic.

    Note: The instruction should mnemonic should already be known to be in the supported instruction_list!

    :param symbol_table: dictionary mapping symbols/labels to their respective addresses (dict)
    :param tokenized_instr_list: tokenized instruction list (list)
    :return: instr_format_dict (dict)
    :raises Exception: if any verification fails
    """
    # Get mnemonic portion
    mnemonic = tokenized_instr_list[0]

    # Get instruction_format_dict
    try:
        instr_format_dict = instructions.instruction_list[mnemonic]
    except KeyError as error:
        raise Exception("Tried to find an instruction in the instruction_list that is not a supported instruction")

    # Get the expected format list
    expected_format_list = instr_format_dict.get("format")

    # Verify the instruction contains the expected number of arguments/fields
    # (matches the expected format for the given mnemonic as specified in the instr_format_dict)

    # Verify token number: number of tokens (including mnemonic) should be the number of expected tokens + 1
    # (+1 because of the mnemonic)
    if len(tokenized_instr_list) != len(expected_format_list) + 1:
        raise Exception("Instruction did not contain expected number of tokens")

    # Verify token types
    for i, token_type in enumerate(expected_format_list):
        """
        Note: TODO's below for additional verification that could be implemented
        
        Checks the following:
            rd, rs, rt - should be in REGISTER_DICT
            rd - cannot be $0, $at, ($k0, $k1)?
                TODO additionally for instructions where rs or rt is the destination, then those can't be the above
                     registers either
                TODO for jr instruction, rs must be multiple of 4
                TODO for lh, lhu, sh, computed address must be a multiple of 2
                TODO fo lw, sw, computed address must be multiple of 4
            imm - should be a number between -2^15 and 2^15-1
            shamt - should be number between 0 and 2^5-1 (Assuming 5 bit unsigned field)
            label - should be a valid label in the symbol table
            imm(rs) - immediate part should fit imm criteria and rs part should be in REGISTERS_DICT
        """
        # Current token is the token from the tokenized instruction list which should match the currently
        # expected token type.
        # (+1 because the tokenized instruction list starts with the mnemonic while the expected format list does not)
        current_token = tokenized_instr_list[i+1]

        # Boolean indicating if currently expected token is of the "imm(rs)" format
        special_case = False

        # Special case: "imm(rs)" format
        # both the immediate portion and the rs portion need to be checked for validity
        # break this up into two parts that then both get verified separately
        if token_type == "imm(rs)":
            special_case = True
            # TODO
            # Verify current token matches expected format
            # Break up the current token into its two parts

        # Verify registers are valid
        if token_type in ["rd", "rs", "rt"]:
            if current_token not in dicts.REGISTER_DICT:
                raise Exception(f"Provided register value \"{current_token}\" is not a valid register")

        # Verify destination register rd is not a protected/reserved register
        if token_type == "rd":
            if current_token in ["$0", "$zero", "$at", "$k0", "$k1"]:
                raise Exception(f"Instruction attempted to write to \"{current_token}\" which is a "
                                f"projected/reserved register")
        # TODO same as above, but for cases when the destination register is not rd

        # Verify immediate value is valid
        if token_type == "imm":
            # Verify value is numeric
            try:
                current_token = int(current_token)
            except ValueError:
                raise Exception(f"Immediate value \"{current_token}\" is not numeric")

            # Verify value is within valid range
            if current_token < (-1*pow(2, 15)) or current_token > (pow(2, 15)-1):
                raise Exception(f"Immediate value \"{current_token}\" is out of range")

        # Verify shift amount is valid
        if token_type == "shamt":
            # Verify value is numeric
            try:
                current_token = int(current_token)
            except ValueError:
                raise Exception(f"Shift amount \"{current_token}\" not numeric")

            # Verify value is within valid range
            if current_token < 0 or current_token > (pow(2, 5) - 1):
                raise Exception(f"Shift amount \"{current_token}\" is out of range")

        # Verify label is valid
        if token_type == "label":
            if current_token not in symbol_table:
                raise Exception(f"Label \"{current_token}\" could not be located in symbol table")

    return instr_format_dict


def assemble_r_instruction(tokenized_instr_list, instr_format_dict):
    """
    Assembles the provided instruction (converts it to binary etc.)

    R Format Instructions

    Written format:
    mnemonic   rd, rs, rt

    Assembled format:
    opcode  rs  rt  rd  shamt   funct
    6       5   5   5   5       6

    :param tokenized_instr_list: tokenized instruction list (list)
    :param instr_format_dict: dictionary from instruction_list containing the formatting info for the given instruction
    :return: binary string containing the final 32 bit instruction (string) (not prefixed with "0b")
        The string will be of the form: "000000 00000 00000 00000 00000 000000"
        can easily be changed to "00000000000000000000000000000000"
    """
    # Initialize and convert all parameters to binary strings
    # with the proper length
    opcode = sign_extend(bin(instr_format_dict.get("opcode")), 6)
    rs = sign_extend(bin(0), 5)
    rt = sign_extend(bin(0), 5)
    rd = sign_extend(bin(0), 5)
    shamt = sign_extend(bin(0), 5)
    funct = sign_extend(bin(instr_format_dict.get("funct")), 6)
    expected_format_list = instr_format_dict.get("format")

    # For each expected token
    for i, token_type in enumerate(expected_format_list):
        # Current token is the token from the tokenized instruction list which should match the currently
        # expected token type.
        # (+1 because the tokenized instruction list starts with the mnemonic while the expected format list does not)
        current_token = tokenized_instr_list[i+1]

        # Update the appropriate value
        match token_type:
            case "rs":
                rs = sign_extend(bin(dicts.REGISTER_DICT[current_token]), 5)
            case "rt":
                rt = sign_extend(bin(dicts.REGISTER_DICT[current_token]), 5)
            case "rd":
                rd = sign_extend(bin(dicts.REGISTER_DICT[current_token]), 5)
            case "shamt":
                shamt = sign_extend(bin(int(current_token)), 5)

    # Return final binary string
    # Note: slicing because bin() results in a string starting with "0b"...
    # also using list comprehension
    # Can remove space separator between tokens by changing " " to ""
    return " ".join([x[2:] for x in [opcode, rs, rt, rd, shamt, funct]])


def assemble_i_instruction(tokenized_instr_list, instr_format_dict):
    """
    Assembles the provided instruction (converts it to binary etc.)

    I Format Instructions

    Written format:
    mnemonic    rt, imm(rs)     <-- for most I type
    mnemonic    rs, rt, imm     <-- for beq and bne

    Assembled format:
    opcode  rs  rt  IMM
    6       5   5   16

    :param tokenized_instr_list: tokenized instruction list (list)
    :param instr_format_dict: dictionary from instruction_list containing the formatting info for the given instruction
    :return: binary string containing the final 32 bit instruction (string) (not prefixed with "0b")
        The string will be of the form: "000000 00000 00000 0000000000000000"
        can easily be changed to "00000000000000000000000000000000"
    """
    # TODO handle "imm(rs)" format
    # TODO compute branch addresses for branch instructions
    # TODO handle negative immediates properly (use 2's complement)

    # Initialize and convert all parameters to binary strings
    # with the proper length
    opcode = sign_extend(bin(instr_format_dict.get("opcode")), 6)
    rs = sign_extend(bin(0), 5)
    rt = sign_extend(bin(0), 5)
    imm = sign_extend(bin(0), 16)
    expected_format_list = instr_format_dict.get("format")

    # For each expected token
    for i, token_type in enumerate(expected_format_list):
        # Current token is the token from the tokenized instruction list which should match the currently
        # expected token type.
        # (+1 because the tokenized instruction list starts with the mnemonic while the expected format list does not)
        current_token = tokenized_instr_list[i+1]

        # Update the appropriate value
        match token_type:
            case "rs":
                rs = sign_extend(bin(dicts.REGISTER_DICT[current_token]), 5)
            case "rt":
                rt = sign_extend(bin(dicts.REGISTER_DICT[current_token]), 5)
            case "imm":
                imm = sign_extend(bin(int(current_token)), 16)

    # Return final binary string
    # Note: slicing because bin() results in a string starting with "0b"...
    # also using list comprehension
    # Can remove space separator between tokens by changing " " to ""
    return " ".join([x[2:] for x in [opcode, rs, rt, imm]])


def assemble_j_instruction(tokenized_instr_list, instr_format_dict, symbol_table):
    """
    Assembles the provided instruction (converts it to binary etc.)

    J Format Instructions

    Written format:
    mnemonic   label

    Assembled format:
    opcode  address
    6       26

    :param tokenized_instr_list: tokenized instruction list (list)
    :param instr_format_dict: dictionary from instruction_list containing the formatting info for the given instruction
    :param symbol_table: dictionary mapping symbols/labels to their respective addresses
    :return: binary string containing the final 32 bit instruction (string) (not prefixed with "0b")
        The string will be of the form: "000000 00000000000000000000000000"
        can easily be changed to "00000000000000000000000000000000"
    """
    # Get opcode, convert to binary string, and extend to proper length
    opcode = sign_extend(bin(instr_format_dict.get("opcode")), 6)

    # Get the address the label portion points to from symbol table
    address = symbol_table[tokenized_instr_list[1]]

    # Convert address to binary string, and extend to proper length
    address = sign_extend(bin(address), 26)

    # Return final binary string
    # Note: slicing because bin() results in a string starting with "0b"...
    # also using list comprehension
    # Can remove space separator between tokens by changing " " to ""
    return " ".join([x[2:] for x in [opcode, address]])

