# MIPSYπ

## Summary
This is a moderately complex and robust 2-pass based MIPS assembler written in Python.

This was a relatively short project completed in partial fulfillment of the requirements
for the CPTR 380 (Computer Architecture) course offered at Walla Walla University.

This assembler accepts a `.asm` file and outputs a `.txt` file containing the assembled code
with the binary represented in ascii text.

This assembler supports a broad range of instructions including jumps, some branches, and even labels.
It is also quite robust as it accepts almost any form of whitespace formatting.
Additionally, every line in the provided MIPS assembly file undergoes numerous verification steps,
so any invalid lines or operations will be caught and reported with helpful error messages.it also performs a lot of verification and reports invalid instructions or operation found

## Table of contents
- [MIPSYπ](#mipsy-)
  * [Summary](#summary)
  * [Table of contents](#table-of-contents)
  * [Quick use guide](#quick-use-guide)
  * [Description of basic operation](#description-of-basic-operation)
  * [Testing and verification](#testing-and-verification)
  * [Supported whitespace formatting etc.](#supported-whitespace-formatting-etc)
  * [Supported instruction list](#supported-instruction-list)
  * [Unsupported instruction list](#unsupported-instruction-list)
  * [Possible future work](#possible-future-work)
  * [Helpful online resources/references](#helpful-online-resources-references)

## Quick use guide

The quickest way to test this program is to simply run it as is.
As currently configured, the program will read the [test.asm](Assembly%20Files/test.asm) assembly file,
assemble it, and produce the [assembled.txt](Assembled%20Files/assembled.txt) output file.

Alternatively if you desire to assemble a different file, you may explicitly code the file path in
[main.py](main.py) or uncomment the lines in [main.py](main.py) which prompt the user to
enter the desired file paths and names in the terminal upon program execution.

While this assembler does not create the header files associated with most object code as used in industry, it does 
allow the user to specify any memory address location for the first instruction.  Note that this address should
be divisible by 4 since the address is a byte address and MIPS instructions each occupy 1 word or 4 bytes.
By default, the start address is arbitrarily set to 7996.  This can be changed by changing the START_ADDRESS 
variable in [assembler.py](assembler.py).  Changing this address will affect the values stored in the immediate
fields of branch instructions since they use PC (program counter) relative addressing.

## Description of basic operation
This assembler is based on a two pass design.
The main entry point is [main.py](main.py) which gets the filepaths and names for the input and output files and 
then calls the `assemble(...)` function in [assembler.py](assembler.py).
The `assemble(...)` function then opens the input file, creates the output file, and handles any errors which may occur
during that process.  Once the both files are open and verified, the`assemble(...)` function calls the
`process_first_pass(...)` function.  This function performs the first pass over the input file.  It is responsible for
the following primary actions:
  1. Keeps track of/assigns each instruction its proper memory address
  2. Builds the symbol table (which maps labels to their respective memory addresses)
     * Returns this table
  3. Determines what each line is in the assembly file
     * Returns a list of tuples specifying each line's type (i.e. comment, I type instruction, etc.) and it associated
         memory address if applicable (from step 1).
  * TODO: Builds a variable table (which maps variables to their respective start addresses
    in memory and specifies their length)

To determine each line's type, another function (`get_line_type(line)`) in the [helpers.py](helpers.py) file is called.
This function uses a number of regex (regular expressions) to match each line and determine its type robustly.  This 
allows the line to be formatted with almost any amount of whitespace, while also performing some basic verification, 
such as assuring that labels don't start with numbers, etc.  The regular expressions used for matching can be found
in the `REGEX_DICT` located in [dicts.py](dicts.py).  If an instructional line is encountered, this function calls yet 
another function: `get_instruction_type(...)` which returns the specific instruction's type/format (i.e. R, I, or J).
It does this by extracting the mnemonic portion of the instruction line and looking it up in the `instruction_list` 
dictionary in [instructions.py](instructions.py).  This list contains a dictionary for each supported instruction which
specifies its type (along with some other things such as its opcode, function value, and expected format).  Once the
`get_instruction_type(...)` function returns and instruction type, the `get_line_type(line)` continues on and
returns a custom type (`LineType`) once completed.  The list of possible types along with short descriptions
can be found in the [custom_type.py](custom_types.py) file.

Once the first pass is complete, the assembler calls the `perform_second_pass(...)` function.  This function performs
the following primary operations:
  1. Reads through the input file and line type list (returned from pass 1) and carries out the following
     operations on every instructional line:
     1. Tokenizes the line (separates it into its basic constituents and removes whitespace, comments, commas, etc.)
     2. Verifies the instructions tokens are valid
     3. Assembles the instruction into its final 32-bit binary representation (in ascii)
     4. Writes the binary representation to the final output file (in ascii)

## Testing and verification
Some testing and verification has been done.  The best example of this is the [test.asm](Assembly%20Files/test.asm)
assembly file, and the [Instruction List and Hand Assembly](Other%20Reference/Instruction%20List%20Reference%20and%20Hand%20Assembly.xlsx)
Microsoft Excel file.  There are two tabs in that file.  The first tab was used to create a list
of all the instructions in the MIPS instruction set architecture along with their expected formats, opcodes, functs, etc.
The second tab contains the [test.asm](Assembly%20Files/test.asm) assembly code broken down
line by line into its decimal and binary representation along with comments denoting special 
cases.  This was created by manually assembling the [test.asm](Assembly%20Files/test.asm) assembly code.
This hand assembled code was then compared to the output this assembler generated.

## Supported whitespace formatting etc.
Lines beginning with "#" are treated as comments  
Comments are also supported at the end of any line (except for lines containing only a label currently)  
Blanks lines are fine  
Labels can be placed on a line by themselves:
```
Label:
  add $t0, $t1, $s0
```
or on the same line as an instruction:
```
Label: add $t0, $t1, $s0
```
The amount of indentation and/or spacing between anything doesn't matter as long as there is 
at least 1 space between each token of an instruction.

## Supported instruction list
add,
addu,
and,
div,
divu,
jalr,
jr,
mfhi,
mflo,
mthi,
mtlo,
mul,
mult,
multu,
nor,
or,
sll,
slt,
sltu,
sra,
srl,
sub,
subu,
xor,
addi,
addiu,
andi,
beq,
bgtz,
blez,
bne,
lb,
lbu,
lhu,
lui,
lw,
ori,
sb,
sh,
slti,
sltiu,
sw,
j,
jal

## Unsupported instruction list
abs,
b,
beqz,
bge,
bgt,
ble,
blt,
bltz,
break,
bxs,
la,
lh,
li,
ll,
lld,
move,
mulos,
muls,
neg,
negu,
neqs,
NOP,
not,
rol,
ror,
sc,
sd,
seq,
sge,
sgt,
sllv,
sne,
srav,
sxs,
syscall,
ulhs,
ulw,
ush,
usw,
xori,
lhi,
lho

## Possible future work
* Better file organization?
* Add GUI
* Make input and output file selection easier
* Verify output file doesn't exist if it is desired to prevent overwriting existing files
* Further testing and verification
* Add support for currently unsupported instructions
* Support variables (custom reserved blocks for data storage)
* Add capability to export in binary format instead of binary represented as ascii
* Add capability to export in hexadecimal format instead of binary
* Support labels on lines by themselves with comments after them
* Change regex so instructions with no arguments/parameters can be supported (i.e. syscall)
  * can do this by removing all regex related checking on instruction lines and just always assume any line that doesn't 
  match any of the other types is an instruction,
  then let the program lookup that line later and see if it is a valid instruction, this is currently done anyways
  would also need to make sure the regex matching a label with an instruction does match something like "label: syscall"
  the quickest way to do this is make the regex instruction match any line that starts with a-Z, but would need to make sure
  that check is done last, since labels start the same way
* Add additional verification for imm(rs) type
* Extend the writing to protected/reserved register verification to also check special cases where the
  destination register is not rd
* Support numeric values for labels
    * Then also add additional verification for jumps and branches to make sure the provided value is valid

## Helpful online resources/references
* [Interactive Online MIPS assembler](https://www.csfieldguide.org.nz/en/interactives/mips-assembler/)
* [Interactive Regex Test Platform](https://regexr.com/)
* [MIPS Instruction Formats](https://www.cs.kzoo.edu/cs230/Resources/MIPS/MachineXL/InstructionFormats.html)
* [MIPS Assembly Instruction Formats](https://en.wikibooks.org/wiki/MIPS_Assembly/Instruction_Formats#Shift_Values)
* [MIPS Instruction Set](https://github-wiki-see.page/m/MIPT-ILab/mipt-mips/wiki/MIPS-Instruction-Set)
* [MIPS Pseudo-instruction, Addressing Modes, and Instruction Formats](https://homepage.divms.uiowa.edu/~ghosh/2-2-10.pdf)
* [MIPS Arithmetic Instructions](https://en.wikibooks.org/wiki/MIPS_Assembly/Arithmetic_Instructions)
* [MIPS Instruction Reference](https://mathcs.holycross.edu/~csci226/MIPS/MIPS_InstructionReference.html)
* [MIPS Instructions Set](https://web.cse.ohio-state.edu/~crawfis.3/cse675-02/Slides/MIPS%20Instruction%20Set.pdf)
* [PowerPoint on Encoding MIPS instructions](https://www.dcc.fc.up.pt/~ricroc/aulas/1920/ac/apontamentos/P04_encoding_mips_instructions.pdf)
* [Branch and Jump Instructions](https://www.doc.ic.ac.uk/lab/secondyear/spim/node16.html)
* [MIPS Encoding Reference](https://student.cs.uwaterloo.ca/~isg/res/mips/opcodes)
* [MIPS Reference Sheet](https://inst.eecs.berkeley.edu/~cs61c/resources/MIPS_help.html)
* [MIPS BIt Instructions and Instruction Encoding](https://fog.ccsf.edu/~gboyd/cs270/online/mipsI/bit_instrs.html)