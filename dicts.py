import re

# Dictionary of all valid registers and their corresponding values
REGISTER_DICT = {
    '$zero': 0,
    '$0': 0,
    '$at': 1,
    '$v0': 2,
    '$v1': 3,
    '$a0': 4,
    '$a1': 5,
    '$a2': 6,
    '$a3': 7,
    '$t0': 8,
    '$t1': 9,
    '$t2': 10,
    '$t3': 11,
    '$t4': 12,
    '$t5': 13,
    '$t6': 14,
    '$t7': 15,
    '$s0': 16,
    '$s1': 17,
    '$s2': 18,
    '$s3': 19,
    '$s4': 20,
    '$s5': 21,
    '$s6': 22,
    '$s7': 23,
    '$t8': 24,
    '$t9': 25,
    '$k0': 26,
    '$k1': 27,
    '$gp': 28,
    '$sp': 29,
    '$fp': 30,
    '$ra': 31
}

# Dictionary of regex search patterns to identify the follow line types
REGEX_DICT = {
    # Matches any line that starts with any amount of whitespace and then a "#"
    # (matches full line)
    'comment': re.compile(r"^\s*#.*"),

    # Matches any line that starts like an instruction
    # (matches full line)
    'instruction': re.compile(r"^\s*[a-zA-Z]+(\s+[a-zA-Z]+\w*|(\s+\$.*)+).*"),

    # Matches any line that contains just a label with any amount of whitespace on either end but nothing else
    # TODO update this so it matches a line with just a label and a comment, but not with an instruction
    # (matches full line)
    'label_only': re.compile(r"^\s*[a-zA-Z]+\w*:\s*$"),

    # Matches any line that contains a label followed by whitespace, a-Z text, whitespace, and then any text
    # (matches full line)
    'label_and_instr': re.compile(r"^\s*[a-zA-Z]+\w*:\s+[a-zA-Z]+\s+.+"),

    # Matches any line of the form "something: .something digits" where digits may be any number of digits
    # (does not match full line, matches up to the end of the digits section)
    'variable': re.compile(r"^\s*[a-zA-Z]+\w*:\s+\.[a-zA-Z]\w*\s+\d+"),

    # Matches any line of the form ".something"
    # (first non-whitespace char is "." and it's followed by an any number of alphanumeric characters)
    # (does not match full line, only to end of word)
    'directive': re.compile(r"^\s*\.\w+")
}
