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
  * [Testing and Verification](#testing-and-verification)
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

## Description of basic operation
This assembler is based on a two pass design.
First pass
uses regex
verifies
builds table
etc.

## Testing and Verification
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