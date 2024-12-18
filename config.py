DEBUG = 1

RETV = {
    "ARG":						0x01,
	"VARIABLE_ASSIGN":			0x02,
	"INSTRUCTION_UNKNOWN":		0x03,
	"INSTRUCTION_WRONG_USAGE":	0x04,
	"VARIABLE_NOT_FOUND":		0x05,
	"LABEL_NOT_FOUND":			0x06,
}

SPECIAL_CHAR = {
	"comment":			"#",
	"label":			":",
	"variable":			"$",
	"variable_assign":	"=",
	"address":			"@",
}

REG = ["a", "b", "c", "d"]

"""
R = Register
A = Address
C = Constant
"""
OPCODE = {
	"NOP": [
		{"value": 0b00_0000, "args": []}
	],
	"MOV": [
		{"value": 0b00_0001, "args": ["R", "A"]},
		{"value": 0b00_0010, "args": ["A", "R"]},
		{"value": 0b00_0011, "args": ["R", "C"]},
		{"value": 0b00_0100, "args": ["A", "C"]},
	],
}