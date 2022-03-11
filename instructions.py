# List of all currently supported instructions
# All values are in decimal
instruction_list = {}
"""
R Format Instructions

Written: 
mnemonic   rd, rs, rt

Assembled:
opcode  rs  rt  rd  shamt   funct
6       5   5   5   5       6
"""
instruction_list["add"] = {"type": "R", "opcode": 0, "funct": 32, "format": ["rd", "rs", "rt"]}
instruction_list["addu"] = {"type": "R", "opcode": 0, "funct": 33, "format": ["rd", "rs", "rt"]}
instruction_list["and"] = {"type": "R", "opcode": 0, "funct": 36, "format": ["rd", "rs", "rt"]}
instruction_list["div"] = {"type": "R", "opcode": 0, "funct": 26, "format": ["rd", "rs", "rt"]}
instruction_list["divu"] = {"type": "R", "opcode": 0, "funct": 27, "format": ["rd", "rs", "rt"]}
instruction_list["jalr"] = {"type": "R", "opcode": 0, "funct": 9, "format": ["rs"]}
instruction_list["jr"] = {"type": "R", "opcode": 0, "funct": 8, "format": ["rs"]}
instruction_list["mfhi"] = {"type": "R", "opcode": 0, "funct": 16, "format": ["rd"]}
instruction_list["mflo"] = {"type": "R", "opcode": 0, "funct": 18, "format": ["rd"]}
instruction_list["mthi"] = {"type": "R", "opcode": 0, "funct": 17, "format": ["rs"]}
instruction_list["mtlo"] = {"type": "R", "opcode": 0, "funct": 19, "format": ["rs"]}
instruction_list["mul"] = {"type": "R", "opcode": 0, "funct": 24, "format": ["rd", "rs", "rt"]}
instruction_list["mult"] = {"type": "R", "opcode": 0, "funct": 24, "format": ["rd", "rs", "rt"]}
instruction_list["multu"] = {"type": "R", "opcode": 0, "funct": 25, "format": ["rd", "rs", "rt"]}
instruction_list["nor"] = {"type": "R", "opcode": 0, "funct": 39, "format": ["rd", "rs", "rt"]}
instruction_list["or"] = {"type": "R", "opcode": 0, "funct": 37, "format": ["rd", "rs", "rt"]}
instruction_list["sll"] = {"type": "R", "opcode": 0, "funct": 0, "format": ["rd", "rt", "shamt"]}
instruction_list["slt"] = {"type": "R", "opcode": 0, "funct": 42, "format": ["rd", "rs", "rt"]}
instruction_list["sltu"] = {"type": "R", "opcode": 0, "funct": 43, "format": ["rd", "rs", "rt"]}
instruction_list["sra"] = {"type": "R", "opcode": 0, "funct": 3, "format": ["rd", "rt", "shamt"]}
instruction_list["srl"] = {"type": "R", "opcode": 0, "funct": 2, "format": ["rd", "rt", "shamt"]}
instruction_list["sub"] = {"type": "R", "opcode": 0, "funct": 34, "format": ["rd", "rs", "rt"]}
instruction_list["subu"] = {"type": "R", "opcode": 0, "funct": 35, "format": ["rd", "rs", "rt"]}
instruction_list["xor"] = {"type": "R", "opcode": 0, "funct": 38, "format": ["rd", "rs", "rt"]}
"""
I Format Instructions

Written: 
mnemonic    rt, IMM(rs)     <-- for most I type
mnemonic    rs, rt, IMM     <-- for beq and bne

Assembled:
opcode  rs  rt  IMM
6       5   5   16 
"""
instruction_list["addi"] = {"type": "I", "opcode": 8, "funct": None, "format": ["rt", "rs", "imm"]}
instruction_list["addiu"] = {"type": "I", "opcode": 9, "funct": None, "format": ["rt", "rs", "imm"]}
instruction_list["andi"] = {"type": "I", "opcode": 12, "funct": None, "format": ["rt", "rs", "imm"]}
instruction_list["beq"] = {"type": "I", "opcode": 4, "funct": None, "format": ["rs", "rt", "label"]}
instruction_list["bgtz"] = {"type": "I", "opcode": 7, "funct": None, "format": ["rs", "label"]}
instruction_list["blez"] = {"type": "I", "opcode": 6, "funct": None, "format": ["rs", "label"]}
instruction_list["bne"] = {"type": "I", "opcode": 5, "funct": None, "format": ["rs", "rt", "label"]}
instruction_list["lb"] = {"type": "I", "opcode": 32, "funct": None, "format": ["rt", "imm(rs)"]}
instruction_list["lbu"] = {"type": "I", "opcode": 36, "funct": None, "format": ["rt", "imm(rs)"]}
instruction_list["lhu"] = {"type": "I", "opcode": 37, "funct": None, "format": ["rt", "imm(rs)"]}
instruction_list["lui"] = {"type": "I", "opcode": 15, "funct": None, "format": ["rt", "imm"]}
instruction_list["lw"] = {"type": "I", "opcode": 35, "funct": None, "format": ["rt", "imm(rs)"]}
instruction_list["ori"] = {"type": "I", "opcode": 13, "funct": None, "format": ["rt", "rs", "imm"]}
instruction_list["sb"] = {"type": "I", "opcode": 40, "funct": None, "format": ["rt", "imm(rs)"]}
instruction_list["sh"] = {"type": "I", "opcode": 41, "funct": None, "format": ["rt", "imm(rs)"]}
instruction_list["slti"] = {"type": "I", "opcode": 10, "funct": None, "format": ["rt", "rs", "imm"]}
instruction_list["sltiu"] = {"type": "I", "opcode": 11, "funct": None, "format": ["rt", "rs", "imm"]}
instruction_list["sw"] = {"type": "I", "opcode": 43, "funct": None, "format": ["rt", "imm(rs)"]}
"""
J Format Instructions

Written: 
mnemonic   label

Assembled:
opcode  address
6       26
"""
instruction_list["j"] = {"type": "J", "opcode": 2, "funct": None, "format": ["label"]}
instruction_list["jal"] = {"type": "J", "opcode": 3, "funct": None, "format": ["label"]}

unsupported_instruction_list = [
    "abs",
    "b",
    "beqz",
    "bge",
    "bgt",
    "ble",
    "blt",
    "bltz",
    "break",
    "bxs",
    "la",
    "lh",
    "li",
    "ll",
    "lld",
    "move",
    "mulos",
    "muls",
    "neg",
    "negu",
    "neqs",
    "NOP",
    "not",
    "rol",
    "ror",
    "sc",
    "sd",
    "seq",
    "sge",
    "sgt",
    "sllv",
    "sne",
    "srav",
    "sxs",
    "syscall",
    "ulhs",
    "ulw",
    "ush",
    "usw",
    "xori",
    "lhi",
    "lho"
]
