import assembler

if __name__ == '__main__':
    # input_filename = input(
    #     "Please enter the full filepath and name including file extension to the MIPS file assembly you would like to assemble: ")
    input_filename = "Assembly Files/test.asm"
    # output_file = input(
    #     "Please enter the full filepath and name (excluding file extension) for the assembled file output: ")
    output_filename = "Assembled Files/assembled.txt"

    # Assemble File
    assembler.assemble(input_filename, output_filename)
