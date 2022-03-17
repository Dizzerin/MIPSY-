import assembler


if __name__ == '__main__':
    # TODO get filename from user
    input_filename = "Assembly Files/test.asm"
    output_filename = "Assembly Files/assembled.txt"

    # Assemble File
    assembler.assemble(input_filename, output_filename)
