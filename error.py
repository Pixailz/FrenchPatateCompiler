class CompileError(Exception):
	def __init__(self, message, error):
		self.message = message
		super().__init__(self.message)
		self.error = error

	def __str__(self):
		return f"{self.message}, {self.error}"