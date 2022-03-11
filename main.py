import assembler


if __name__ == '__main__':
    # TODO get filename from user
    input_filename = "Assembly Files/advanced.asm"
    output_filename = "Assembly Files/out.txt"

    # Assembly File
    assembler.assemble(input_filename, output_filename)
