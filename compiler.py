import sys

from pprint import pprint


from config import RETV
from error import CompileError

import parsing


class Compiler():
	def __init__(self):
		self.label = {}
		self.variable = {}

	def open(self, path):
		self.path = path

		with open(self.path, "r") as f:
			self.str = f.read()

	def precompile(self):
		self.lines = []
		length = 0
		self.nb_line = 0

		for line in self.str.split("\n"):
			self.nb_line += 1
			# 1. Basic parsing, strip space, and split on space
			parsed = parsing.process_line(line)
			if parsed is None:
				continue

			# 2. Assign variable value
			try:
				variable = parsing.get_variable_assign(parsed)
			except CompileError as e:
				print(f"Line {self.nb_line}: {e}")
				sys.exit(RETV["VARIABLE_ASSIGN"])
			if variable is not None:
				self.variable[variable[0]] = variable[1]
				continue

			self.lines.append(parsed)

	def replace_var(self, line):
		for k, v in enumerate(line):
			if parsing.is_variable(v):
				name = parsing.get_variable_name(v)
				value = self.variable.get(name, None)
				if value is None:
					raise CompileError("Variable not found", name)
				line[k] = value

		return line

	def compile(self):
		self.precompile()
		self.compiled = []

		length = 0

		for line in self.lines:
			instr = line[0]
			args = line[1:]

			# 3. Check if line is a label, if so assign save label
			label = parsing.get_label(instr)
			if label is not None:
				self.label[label] = length
				continue

			# 4. Replace variable within a line
			try:
				args = self.replace_var(args)
			except CompileError as e:
				print(f"Line {self.nb_line}: {e}")
				sys.exit(RETV["VARIABLE_NOT_FOUND"])

			# 5. Check if instruction is found
			opcode = parsing.get_instruction(instr)
			if opcode is None:
				print(f"Line {self.nb_line}: Unknown Instructions {instr}")
				sys.exit(RETV["INSTRUCTION_UNKNOWN"])

			# 6. Get variant given args and opcode
			opcode_variant = parsing.get_instruction_variant(args, opcode)
			if opcode_variant is None:
				print(f"Line {self.nb_line}: Wrong usage for {instr}")
				sys.exit(RETV["INSTRUCTION_WRONG_USAGE"])

			# 7. Compile value, leaving label intact for the moment
			compiled_tmp = []
			compiled_instr = opcode_variant['value']
			for k, arg in enumerate(opcode_variant["args"]):
				if parsing.is_label(args[k]):
					compiled_tmp.append(args[k])
					continue

				if arg == "R":
					compiled_instr = parsing.encode_reg(args[k], compiled_instr)
				if arg == "A":
					compiled_tmp.extend(parsing.encode_address(args[k]))
				if arg == "C":
					compiled_tmp.append(parsing.encode_constant(args[k]))

			# 8. Update current compiled byte and update current length
			self.compiled.append(compiled_instr)
			self.compiled.extend(compiled_tmp)
			length += parsing.get_instruction_size(opcode_variant["args"])

		# 9. Replace label now that we have ALL label with correct value
		self.replace_label()

	def replace_label(self):
		compiled_tmp = []

		for k, byte in enumerate(self.compiled):
			if parsing.is_label(byte):
				try:
					compiled_tmp.extend(parsing.encode_label(self, byte))
				except CompileError as e:
					print(f"Line {self.nb_line}: {e}")
					sys.exit(RETV["LABEL_NOT_FOUND"])
			else:
				compiled_tmp.append(byte)

		self.compiled = compiled_tmp

def xxd(byte, size=0x10, dividing=8):
	divider = size / dividing

	for k, v in enumerate(byte):
		if not k % size:
			to_print = f"{k:#06x}: "
			if k != 0:
				to_print = "\n" + to_print
			print(to_print, end="")
		print(f"{v:02x}", end="")
		if not (k+1) % divider:
			print(" ", end="")
	print()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("file needed")
		sys.exit(RETV["ARG"])

	compiler = Compiler()
	compiler.open(sys.argv[1])
	compiler.compile()

	xxd(compiler.compiled)