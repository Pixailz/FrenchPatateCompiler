from config import SPECIAL_CHAR
from config import OPCODE
from config import RETV
from config import REG_1, REG_2
from config import REG_1_SPEC, REG_2_SPEC

from error import CompileError

from pprint import pprint

# Convertion

def str_to_int(part):
	try:
		if part.startswith("0x"):
			return int(part, 16)
		elif part.startswith("0o"):
			return int(part, 8)
		elif part.startswith("0b"):
			return int(part, 2)
		else:
			return int(part)
	except:
		return None

# Check
def is_comment(line):
	if line.startswith(SPECIAL_CHAR["comment"]):
		return True
	return False

def is_variable(part):
	return part.startswith(SPECIAL_CHAR["variable"])

def is_label(part):
	if type(part) is int:
		return False
	return part.startswith(SPECIAL_CHAR["label"])

def	is_reg_1(part):
	return part.lower() in REG_1

def	is_reg_2(part):
	return part.lower() in REG_2

def is_reg_2_address(part):
	if not part.startswith(SPECIAL_CHAR["address"]):
		return False

	return is_reg_2(part.removeprefix(SPECIAL_CHAR["address"]))

def	is_constant(part):
	part = str_to_int(part)
	return part is not None

def	is_constant_1(part):
	part = str_to_int(part)
	return part is not None and part <= 0xff

def	is_constant_2(part):
	part = str_to_int(part)
	return part is not None and part > 0xff

def is_address(part):
	if is_label(part):
		return True
	if not part.startswith(SPECIAL_CHAR["address"]):
		return False
	part = part.removeprefix(SPECIAL_CHAR["address"])

	part = str_to_int(part)

	return part is not None

# Process
def process_line(line):
	if line == "":
		return None
	l = line.strip().split()
	if len(l) == 0:
		return None
	if is_comment(l[0]):
		return None
	return l

def get_label(part):
	if not is_label(part):
		return None
	return part.removeprefix(SPECIAL_CHAR["label"])

def get_variable_assign(line):
	if not is_variable(line[0]):
		return None

	if not line[1] == SPECIAL_CHAR["variable_assign"]:
		raise CompileError(
			"Wrong assignation symbole",
			f"expected {SPECIAL_CHAR["variable_assign"]} got {line[1]}",
			RETV["VARIABLE_ASSIGN"]
		)

	return line[0].removeprefix(SPECIAL_CHAR["variable"]), line[2]

def get_variable_name(part):
	return part.removeprefix(SPECIAL_CHAR["variable"])

def get_instruction(part):
	return OPCODE.get(part, None)

def get_operand_type(part):
	if is_reg_1(part):
		return "R1"
	elif is_reg_2(part):
		return "R2"
	elif is_reg_2_address(part):
		return "@R2"
	elif is_address(part):
		return "A"
	elif is_constant(part):
		return "C"

	return None

def get_instruction_variant(args, opcode):
	nb_args = len(args)
	found = None

	for variant in opcode:
		if len(variant["args"]) != nb_args:
			continue

		tmp_i = 0

		for i, arg in enumerate(variant["args"]):
			if arg == get_operand_type(args[i]):
				tmp_i += 1

		if tmp_i == nb_args:
			found = variant
			break

	return found

def get_operand_size(op):
	if op == "R1" or op == "R2" or op == "@R2":
		return 1
	elif op == "A":
		return 2
	elif op == "C1" or op == "C":
		return 1
	elif op == "C2":
		return 2
	return 0

def	get_instruction_size(operand):
	length = 1
	match operand:
		case ["R2", "C"]:
			return 4
	for op in operand:
		length += get_operand_size(op)
	return length

def get_reg(reg):
	if reg == "a":
		return 0b00
	elif reg == "b":
		return 0b01
	elif reg == "c":
		return 0b10
	elif reg == "d":
		return 0b11
	return 0

def get_reg_spec(reg):
	if reg.endswith(REG_1_SPEC[0]):
		return 0b10
	elif reg.endswith(REG_1_SPEC[1]):
		return 0b01
	return 0b00

def is_reg_2_address(part):
	if not part.startswith(SPECIAL_CHAR["address"]):
		return False

	return is_reg_2(part.removeprefix(SPECIAL_CHAR["address"]))

# Encode
def encode_reg(part, is_short):
	if is_reg_2_address(part):
		part = part.removeprefix(SPECIAL_CHAR["address"])
	part = part.lower()
	_part = part
	reg_spec = 0

	if is_short:
		for s in REG_1_SPEC:
			_part = _part.removesuffix(s)
		reg_spec = get_reg_spec(part)
	else:
		for s in REG_2_SPEC:
			_part = _part.removeprefix(s[0])
			_part = _part.removesuffix(s[1])

	reg = get_reg(_part)

	return reg | reg_spec << 2

def encode_address(part):
	if type(part) is str:
		addr_n = str_to_int(part.removeprefix(SPECIAL_CHAR["address"]))
	elif type(part) is int:
		addr_n = part

	if addr_n > 0xffff:
		raise CompileError("Address to high", addr_n, RETV["ADDRESS_TOO_HIGH"])
	return [addr_n >> 8, addr_n & 0xff]

def encode_constant_1(part):
	return str_to_int(part)

def encode_constant_2(part):
	part = str_to_int(part)
	return [ part >> 8, part & 0xff ]

def encode_label(self, label):
	value = self.label.get(label.removeprefix(SPECIAL_CHAR["label"]), None)
	if value is None:
		raise CompileError("Label not found", label, RETV["LABEL_NOT_FOUND"])
	return encode_address(value)