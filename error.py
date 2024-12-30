class CompileError(Exception):
	def __init__(self, message, error, errno):
		self.message = message
		super().__init__(self.message)
		self.error = error
		self.errno = errno

	def __str__(self):
		return f"Error ({self.errno}): {self.message}, {self.error}"

def perror(e):
	print(e)
	sys.exit(e.errno)