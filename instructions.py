INSTRUCTION_DICT = {
    'R-TYPE': {
        'add': (0x0, 0b100000, ['rd', 'rs', 'rt']),
        'addu': (0x0, 0b100001, ['rd', 'rs', 'rt']),
        'and': (0x0, 0b100100, ['rd', 'rs', 'rt']),
        'break': (0x0, 0b001101, []),
        'div': (0x0, 0b011010, ['rd', 'rs', 'rt']),
        'divu': (0x0, 0b011011, ['rs', 'rt']),
        'jalr': (0x0, 0b001001, ['rd', 'rs']),
        'jr': (0x0, 0b001000, ['rs']),
        'mfhi': (0x0, 0b010000, ['rd']),
        'mflo': (0x0, 0b010010, ['rd']),
        'mthi': (0x0, 0b010001, ['rs']),
        'mtlo': (0x0, 0b010011, ['rs']),
        'mult': (0x0, 0b011000, ['rs', 'rt']),
        'multu': (0x0, 0b011001, ['rs', 'rt']),
        'nor': (0x0, 0b100111, ['rd', 'rs', 'rt']),
        'or': (0x0, 0b100101, ['rd', 'rs', 'rt']),
        'sll': (0x0, 0b000000, ['rd', 'rt']),
        'sllv': (0x0, 0b000100, ['rd', 'rt']),
        'slt': (0x0, 0b101010, ['rd', 'rs', 'rt']),
        'sltu': (0x0, 0b101011, ['rd', 'rs', 'rt']),
        'sra': (0x0, 0b000011, ['rd', 'rt']),
        'srav': (0x0, 0b000111, ['rd', 'rt']),
        'srl': (0x0, 0b000010, ['rd', 'rt']),
        'srlv': (0x0, 0b000110, ['rd', 'rt', 'rs']),
        'sub': (0x0, 0b100010, ['rd', 'rs', 'rt']),
        'subu': (0x0, 0b100011, ['rd', 'rs', 'rt']),
        'syscall': (0x0, 0b001100, []),
        'xor': (0x0, 0b100110, ['rd', 'rs', 'rt'])
    },

    'I-TYPE': {
        'addi': (0b001000, ['rt', 'rs']),
        'addiu': (0b001001, ['rt', 'rs']),
        'andi': (0b001100, ['rt', 'rs']),
        'beq': (0b000100, ['rs', 'rt']),
        'bgez': (0b000001, 0b00001, ['rs']),
        'bgtz': (0b000111, 0b00000, ['rs']),
        'blez': (0b000110, 0b00000, ['rs']),
        'bltz': (0b000001, 0b00000, ['rs']),
        'bne': (0b000101, ['rs', 'rt']),
        'lb': (0b100000, ['rt', 'rs']),
        'lbu': (0b100100, ['rt', 'rs']),
        'lh': (0b100001, ['rt', 'rs']),
        'lhu': (0b100101, ['rt', 'rs']),
        'lui': (0b001111, ['rt']),
        'lw': (0b100011, ['rt', 'rs']),
        'lwc1': (0b110001, ['rt', 'rs']),
        'ori': (0b001101, ['rt', 'rs']),
        'sb': (0b101000, ['rt', 'rs']),
        'slti': (0b001010, ['rt', 'rs']),
        'sltiu': (0b001011, ['rt', 'rs']),
        'sh': (0b101001, ['rt', 'rs']),
        'sw': (0b101011, ['rt', 'rs']),
        'sc': (0b111000, ['rt', 'rs']),
        'swc1': (0b111001, ['rt', 'rs']),
        'xori': (0b001110, ['rt', 'rs'])
    },

    'J-TYPE': {
        'j': (0b000010, []),
        'jal': (0b000011, [])
    }
}

# Values in HEX
instruction_table = {
    'add': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x20'],
    'addi': ['0x08', 'rs', 'rt', 'imm'],
    'addiu': ['0x09', 'rs', 'rt', 'imm'],
    'addu': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x21'],
    'and': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x24'],
    'andi': ['0x0C', 'rs', 'rt', 'imm'],
    'beq': ['0x04', 'rs', 'rt', 'imm'],
    'bne': ['0x05', 'rs', 'rt', 'imm'],
    'j': ['0x02', 'add'],
    'jal': ['0x03', 'add'],
    'jr': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x08'],
    'lbu': ['0x24', 'rs', 'rt', 'imm'],
    'lhu': ['0x25', 'rs', 'rt', 'imm'],
    'll': ['0x30', 'rs', 'rt', 'imm'],
    'lui': ['0x0F', 'rs', 'rt', 'imm'],
    'lw': ['0x23', 'rs', 'rt', 'imm'],
    'nor': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x27'],
    'or': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x25'],
    'ori': ['0x0D', 'rs', 'rt', 'imm'],
    'slt': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x2A'],
    'slti': ['0x0A', 'rs', 'rt', 'imm'],
    'sltiu': ['0x0B', 'rs', 'rt', 'imm'],
    'sltu': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x2B'],
    'sb': ['0x28', 'rs', 'rt', 'imm'],
    'sc': ['0x38', 'rs', 'rt', 'imm'],
    'sh': ['0x29', 'rs', 'rt', 'imm'],
    'sw': ['0x2B', 'rs', 'rt', 'imm'],
    'sub': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x22'],
    'subu': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x23'],

    # Arithmetic Core
    'div': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x1A'],
    'divu': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x1B'],
    'mfhi': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x10'],
    'mflo': ['0x00', 'rs', 'rt', 'rd', 'shamt', '0x12']
}

instructions_list = {}
instructions_list['add']   =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 32}
instructions_list['addu']  =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 33}
instructions_list['and']   =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 36}
instructions_list['jr']    =   {'format': 'R', 'opcode': 0,  'order': 's',   'fun': 8}
instructions_list['nor']   =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 39}
instructions_list['or']    =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 37}
instructions_list['slt']   =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 42}
instructions_list['sltu']  =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 43}
instructions_list['sll']   =   {'format': 'R', 'opcode': 0,  'order': 'dts', 'fun': 0}
instructions_list['srl']   =   {'format': 'R', 'opcode': 0,  'order': 'dts', 'fun': 2}
instructions_list['sub']   =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 34}
instructions_list['subu']  =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 35}
instructions_list['xor']   =   {'format': 'R', 'opcode': 0,  'order': 'dst', 'fun': 38}
instructions_list['addi']  =   {'format': 'I', 'opcode': 8,  'order': 'tsi'}
instructions_list['addiu'] =   {'format': 'I', 'opcode': 9,  'order': 'tsi'}
instructions_list['andi']  =   {'format': 'I', 'opcode': 12, 'order': 'tsi'}
instructions_list['beq']   =   {'format': 'I', 'opcode': 4,  'order': 'branch'}
instructions_list['bne']   =   {'format': 'I', 'opcode': 5,  'order': 'branch'}
instructions_list['lb']    =   {'format': 'I', 'opcode': 32, 'order': 'offset'}
instructions_list['lbu']   =   {'format': 'I', 'opcode': 36, 'order': 'offset'}
instructions_list['lhu']   =   {'format': 'I', 'opcode': 37, 'order': 'offset'}
instructions_list['ll']    =   {'format': 'I', 'opcode': 48, 'order': 'tsi'}
instructions_list['lui']   =   {'format': 'I', 'opcode': 15, 'order': 'tsi'}
instructions_list['lw']    =   {'format': 'I', 'opcode': 35, 'order': 'offset'}
instructions_list['ori']   =   {'format': 'I', 'opcode': 13, 'order': 'tsi'}
instructions_list['slti']  =   {'format': 'I', 'opcode': 10, 'order': 'tsi'}
instructions_list['sltiu'] =   {'format': 'I', 'opcode': 11, 'order:': 'tsi'}
instructions_list['sb']    =   {'format': 'I', 'opcode': 40, 'order': 'offset'}
instructions_list['sc']    =   {'format': 'I', 'opcode': 56, 'order': 'offset'}
instructions_list['sh']    =   {'format': 'I', 'opcode': 41, 'order': 'offset'}
instructions_list['sw']    =   {'format': 'I', 'opcode': 43, 'order': 'offset'}
instructions_list['j']     =   {'format': 'J', 'opcode': 2,  'order': 't'}
instructions_list['jal']   =   {'format': 'J', 'opcode': 3,  'order': 't'}
