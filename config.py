DEBUG = 1

RETV = {
    "ARG":						0x01,
	"VARIABLE_ASSIGN":			0x02,
	"VARIABLE_NOT_FOUND":		0x03,
	"INSTRUCTION_UNKNOWN":		0x04,
	"INSTRUCTION_WRONG_USAGE":	0x05,
	"LABEL_NOT_FOUND":			0x06,
	"CONSTANT_TOO_LONG":		0x07,
	"ADDRESS_TOO_HIGH":			0x08
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
R1	= Register, 8b
R2	= Register, 16b
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
	],

	"ADD": [
		{"value": 0x06, "args": ["R1",	"C"]},
		{"value": 0x07, "args": ["R1",	"A"]},
		{"value": 0x08, "args": ["A",	"C"]},
		{"value": 0x09, "args": ["A",	"R1"]},
		{"value": 0x0a, "args": ["R1",	"R1"]},
		{"value": 0x0b, "args": ["A",	"A"]},
	],

	"SUB": [
		{"value": 0x0c, "args": ["R1",	"C"]},
		{"value": 0x0d, "args": ["R1",	"A"]},
		{"value": 0x0e, "args": ["A",	"C"]},
		{"value": 0x0f, "args": ["A",	"R1"]},
		{"value": 0x10, "args": ["R1",	"R1"]},
		{"value": 0x11, "args": ["A",	"A"]},
	],

	# "SUB": [
	# 	{"value": 0x07, "args": ["R1",	"C"]}
	# ],

	# "AND": [
	# 	{"value": 0x08, "args": ["R1",	"C"]}
	# ],

	# "OR": [
	# 	{"value": 0x09, "args": ["R1",	"C"]}
	# ],

	# "XOR": [
	# 	{"value": 0x0a, "args": ["R1",	"C"]}
	# ],

	# "NOT": [
	# 	{"value": 0x0b, "args": ["R1"]}
	# ],

	# "SHL": [
	# 	{"value": 0x0c, "args": ["R1",	"C"]}
	# ],

	# "SHR": [
	# 	{"value": 0x0d, "args": ["R1",	"C"]}
	# ],

	"HLT": [
		{"value": 0xff, "args": []},
	],
}
