DEBUG = 0

RETV = {
    "ARG":						0x01,
	"VARIABLE_ASSIGN":			0x02,
	"VARIABLE_NOT_FOUND":		0x03,
	"INSTRUCTION_UNKNOWN":		0x04,
	"INSTRUCTION_WRONG_USAGE":	0x05,
	"LABEL_NOT_FOUND":			0x06,
	"DUPLICATE_LABEL":			0x07,
	"CONSTANT_TOO_LONG":		0x08,
	"ADDRESS_TOO_HIGH":			0x09
}

SPECIAL_CHAR = {
	"comment":			"#",
	"label":			":",
	"variable":			"$",
	"variable_assign":	"=",
	"address":			"@",
}

REG = ["a", "b", "c", "d"]

REG_1_SPEC = [
	"h", "l"
]
REG_1 = [ f"{r}{s}" for r in REG for s in REG_1_SPEC ]

REG_2_SPEC = [
	["r", "x"],
]

REG_2 = [ f"{s[0]}{r}{s[1]}" for r in REG for s in REG_2_SPEC ]

"""
R1	= Register, followed by 8b data
R2	= Register, followed by 16b data
@R2	= Register pointer, followed by 16b data
A	= Address
C	= Constant
"""
OPCODE = {
	"NOP": [
		{"value": 0x00, "args": []}
	],

	"MOV": [
		{"value": 0x01, "args": ["R1",	"C"]},
		{"value": 0x02, "args": ["R2",	"C"]},
		{"value": 0x03, "args": ["A",	"R1"]},
		{"value": 0x04, "args": ["R1",	"A"]},
		{"value": 0x05, "args": ["A",	"C"]},
		{"value": 0x06, "args": ["@R2",	"C"]},
		{"value": 0x07, "args": ["@R2",	"A"]},
		{"value": 0x08, "args": ["@R2",	"@R2"]},
	],

	"ADD": [
		{"value": 0x09, "args": ["R1",	"C"]},
		{"value": 0x0a, "args": ["R1",	"A"]},
		{"value": 0x0b, "args": ["A",	"C"]},
		{"value": 0x0c, "args": ["A",	"R1"]},
		{"value": 0x0d, "args": ["R1",	"R1"]},
		{"value": 0x0e, "args": ["A",	"A"]},
	],

	"SUB": [
		{"value": 0x0f, "args": ["R1",	"C"]},
		{"value": 0x10, "args": ["R1",	"A"]},
		{"value": 0x11, "args": ["A",	"C"]},
		{"value": 0x12, "args": ["A",	"R1"]},
		{"value": 0x13, "args": ["R1",	"R1"]},
		{"value": 0x14, "args": ["A",	"A"]},
	],

	"AND": [
		{"value": 0x15, "args": ["R1",	"C"]},
		{"value": 0x16, "args": ["R1",	"A"]},
		{"value": 0x17, "args": ["A",	"C"]},
		{"value": 0x18, "args": ["A",	"R1"]},
		{"value": 0x19, "args": ["R1",	"R1"]},
		{"value": 0x1a, "args": ["A",	"A"]},
	],

	"OR": [
		{"value": 0x1b, "args": ["R1",	"C"]},
		{"value": 0x1c, "args": ["R1",	"A"]},
		{"value": 0x1d, "args": ["A",	"C"]},
		{"value": 0x1e, "args": ["A",	"R1"]},
		{"value": 0x1f, "args": ["R1",	"R1"]},
		{"value": 0x20, "args": ["A",	"A"]},
	],

	"XOR": [
		{"value": 0x21, "args": ["R1",	"C"]},
		{"value": 0x22, "args": ["R1",	"A"]},
		{"value": 0x23, "args": ["A",	"C"]},
		{"value": 0x24, "args": ["A",	"R1"]},
		{"value": 0x25, "args": ["R1",	"R1"]},
		{"value": 0x26, "args": ["A",	"A"]},
	],

	"SHL": [
		{"value": 0x27, "args": ["R1",	"C"]},
		{"value": 0x28, "args": ["R1",	"A"]},
		{"value": 0x29, "args": ["A",	"C"]},
		{"value": 0x2a, "args": ["A",	"R1"]},
		{"value": 0x2b, "args": ["R1",	"R1"]},
		{"value": 0x2c, "args": ["A",	"A"]},
	],

	"SHR": [
		{"value": 0x2d, "args": ["R1",	"C"]},
		{"value": 0x2e, "args": ["R1",	"A"]},
		{"value": 0x2f, "args": ["A",	"C"]},
		{"value": 0x30, "args": ["A",	"R1"]},
		{"value": 0x31, "args": ["R1",	"R1"]},
		{"value": 0x32, "args": ["A",	"A"]},
	],

	"NOT": [
		{"value": 0x33, "args": ["R1"]},
		{"value": 0x34, "args": ["A"]},
	],


	"JMP": [
		{"value": 0x35, "args": ["R2"]},
		{"value": 0x36, "args": ["A"]},
	],

	"JPZ": [
		{"value": 0x37, "args": ["R2"]},
		{"value": 0x38, "args": ["A"]},
	],

	"JPC": [
		{"value": 0x39, "args": ["R2"]},
		{"value": 0x3a, "args": ["A"]},
	],


	"PUSH": [
		{"value": 0x3b, "args": ["C"]},
		{"value": 0x3c, "args": ["R1"]},
		{"value": 0x3d, "args": ["R2"]},
		{"value": 0x3e, "args": ["A"]},
	],

	"POP": [
		{"value": 0x3f, "args": ["R1"]},
		{"value": 0x40, "args": ["R2"]},
		{"value": 0x41, "args": ["A"]},
	],

	"JPS": [
		{"value": 0x42, "args": ["A"]},
	],

	"RTS": [
		{"value": 0x43, "args": []},
	],


	"RENDER": [
		{"value": 0xf8, "args": []},
	],


	"INP": [
		{"value": 0xf9, "args": ["R1"]},
		{"value": 0xfa, "args": ["R2"]},
		{"value": 0xfb, "args": ["A"]},
	],

	"RAND": [
		{"value": 0xfc, "args": ["R1"]},
		{"value": 0xfd, "args": ["R2"]},
		{"value": 0xfe, "args": ["A"]},
	],

	"HLT": [
		{"value": 0xff, "args": []},
	],
}
