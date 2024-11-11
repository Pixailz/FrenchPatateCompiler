import sys

DEBUG = 1

RETV = {
    "ARG":              0x01,
    "LABEL_NOT_FOUND":  0x02,
    "VAR_NOT_FOUND":    0x03,
    "SYM_NOT_FOUND":    0x04,
    "WRONG_ARG":        0x05,
    "LABEL_NOT_FOUND":  0x06,
}

if len(sys.argv) != 2:
    print("file needed")
    sys.exit(RETV["ARG"])

with open(sys.argv[1], "r") as f:
    FILE_STR = f.read()

OPCODE = {
    "NOOP": {       "value": 0b0000_0000, "args": []},
    "LD": {         "value": 0b0000_0001, "args": ["R", "OP1"]},
    "LDI": {        "value": 0b0000_0010, "args": ["R", "OP1"]},
    "ST": {         "value": 0b0000_0011, "args": ["R", "OP1"]},
    "STI": {        "value": 0b0000_0100, "args": ["OP1", "OP2"]},
    "ADD": {        "value": 0b0000_0101, "args": ["R", "OP1"]},
    "SUB": {        "value": 0b0000_0110, "args": ["R", "OP1"]},
    "JMP": {        "value": 0b0000_0111, "args": ["OP1"]},
    "JPZ": {        "value": 0b0000_1000, "args": ["OP1"]},
    "JPC": {        "value": 0b0000_1001, "args": ["OP1"]},
    "ADDR": {       "value": 0b0000_1010, "args": ["R", "OP1"]},
    "SUBR": {       "value": 0b0000_1011, "args": ["R", "OP1"]},
    "LDE": {        "value": 0b0000_1100, "args": ["R", "OP1"]},
    "AND": {        "value": 0b0000_1101, "args": ["R", "OP1"]},
    "OR": {         "value": 0b0000_1110, "args": ["R", "OP1"]},
    "XOR": {        "value": 0b0000_1111, "args": ["R", "OP1"]},
    "NOT": {        "value": 0b0001_0000, "args": ["R", "OP1"]},
    "ANDR": {       "value": 0b0001_0001, "args": ["R", "OP1"]},
    "ORR": {        "value": 0b0001_0010, "args": ["R", "OP1"]},
    "XORR": {       "value": 0b0001_0011, "args": ["R", "OP1"]},
    "NOTR": {       "value": 0b0001_0100, "args": ["R", "OP1"]},

    "INP": {        "value": 0b0011_1010, "args": ["R"]},
    "BCD": {        "value": 0b0011_1011, "args": ["R"]},
    "RAND": {       "value": 0b0011_1100, "args": ["R"]},
    "OUTST": {      "value": 0b0011_1101, "args": ["R"]},
    "HLT": {        "value": 0b0011_1111, "args": []},
}

def encode_reg(reg):
    if reg == "A":
        return 0b00_00_0000
    elif reg == "B":
        return 0b01_00_0000
    elif reg == "C":
        return 0b10_00_0000
    elif reg == "D":
        return 0b11_00_0000
    return None

def get_arg(arg):
    if arg.startswith(":") or arg.startswith("$"):
        return arg
    if arg.startswith("0x"):
        return int(arg, 16)
    return int(arg)

def replace_label_var(arg):
    if arg.startswith(":"):
        _label = arg.removeprefix(":")
        label = LABEL.get(_label, None)
        if label is None:
            print(f"Label {_label} not found")
            sys.exit(RETV["LABEL_NOT_FOUND"])
        return label
    if arg.startswith("$"):
        _var = arg.removeprefix("$")
        var = VAR.get(_var, None)
        if var is None:
            print(f"Var {_var} not found")
            sys.exit(RETV["VAR_NOT_FOUND"])
        return var 

COMPILED = []
LABEL = {}
VAR = {}

for line in FILE_STR.split("\n"):
    if line.startswith("#"):
        continue

for line in FILE_STR.split("\n"):
    if line == "":
        continue
    if line.startswith(":"):
        LABEL[line.removeprefix(":")] = len(COMPILED)
        continue

    elif line.startswith("$"):
        line = line.removeprefix("$")
        var = line.split()
        VAR[var[0]] = get_arg(var[1])
        continue

    elif line.startswith("#"):
        continue
 
    tmp = line.split()
    inst = tmp[0]
    args = tmp[1:]
    opcode = OPCODE.get(inst, None)

    if DEBUG:
        print(f"Instruction {inst}", end="")
        i = 0
        for arg in args:
            print(f", arg{i+1} {args[i]}", end="")
            i += 1
        print()

    if opcode is None:
        print(f"Literal {inst} could not be compiled")
        sys.exit(RETV["SYM_NOT_FOUND"])
        
    if len(args) != len(opcode["args"]):
        print(f"Wrong argument for {inst}")
        sys.exit(RETV["WRONG_ARG"])

    compiled = [opcode["value"]]
    for i in range(len(opcode["args"])):
        compiled.append(0)
    i = 0
    for arg in opcode["args"]:
        if arg == "R":
            reg = encode_reg(args[i])
            if reg is None:
                print(f"Wrong register {args[i]}")
                sys.exit(4)
            compiled[0] |= reg
            compiled.pop()
        elif arg == "OP1":
            compiled[1] = get_arg(args[i])
        elif arg == "OP2":
            compiled[2] = get_arg(args[i])
        i += 1 

    COMPILED += compiled

i = 0
for instr in COMPILED:
    if type(instr) == str:
        COMPILED[i] = replace_label_var(instr)
    i += 1

if DEBUG:
    i = 0
    for b in COMPILED:
        print(f"0x{i:02x}: {b:08b}")
        i += 1

with open(sys.argv[1].removesuffix(".fp"), "wb") as f:
    f.write(bytes(COMPILED))
