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
		{"value": 0b0000_0000, "args": []}
	],

	"MOV": [
		{"value": 0b0000_0001, "args": ["R1",	"C"]},
		{"value": 0b0000_0010, "args": ["R2",	"C"]},
		{"value": 0b0000_0011, "args": ["A",	"R1"]},
		{"value": 0b0000_0100, "args": ["R1",	"A"]},
		{"value": 0b0000_0101, "args": ["A",	"C"]},
	],

	"ADD": [
		{"value": 0b0000_0110, "args": ["R1", "C"]}
	],

	"HLT": [
		{"value": 0b1111_1111, "args": []},
	],
}
