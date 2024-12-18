from config import SPECIAL_CHAR
from config import OPCODE
from config import REG

from error import CompileError

from pprint import pprint

# Convertion

def str_to_int(part):
	try:
		if part.startswith("0x"):
			return int(part, 16)
		elif part.startwith("0o"):
			return int(part, 8)
		elif part.startwith("0b"):
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

def	is_reg(part):
	return part.lower() in REG

def	is_constant(part):
	part = str_to_int(part)

	return part is not None

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
			f"expected {SPECIAL_CHAR["variable_assign"]} got {line[1]}"
		)

	assert line[1] == SPECIAL_CHAR["variable_assign"]

	return line[0].removeprefix(SPECIAL_CHAR["variable"]), line[2]

def get_variable_name(part):
	return part.removeprefix(SPECIAL_CHAR["variable"])

def get_instruction(part):
	return OPCODE.get(part, None)

def get_operand_type(part):
	if is_reg(part):
		return "R"
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
	if op == "R":
		return 0
	elif op == "A":
		return 2
	elif op == "C":
		return 1
	return 0

def	get_instruction_size(operand):
	length = 1
	for op in operand:
		length += get_operand_size(op)
	return length

# Encode
def encode_reg(part, opcode):
	return REG.index(part.lower()) << 6 | opcode

def encode_address(part):
	if type(part) is str:
		addr_n = str_to_int(part.removeprefix(SPECIAL_CHAR["address"]))
	elif type(part) is int:
		addr_n = part
	return [addr_n >> 8, addr_n & 0xff]

def encode_constant(part):
	return str_to_int(part)

def encode_label(self, label):
	value = self.label.get(label.removeprefix(SPECIAL_CHAR["label"]), None)
	if value is None:
		raise CompileError("Label not found", label)
	return encode_address(value)