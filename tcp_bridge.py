import socket
import sys

from time import sleep

from pprint import pprint


from compiler import Compiler, xxd

SOCKET = None

class TCPBridge():
	def __init__(self, host, port):
		self.address = (host, port)
		self.socket = None
		self.open_socket()
		self.bind_socket()
		self.listen_socket()

	def __del__(self):
		self.close()

	def open_socket(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.hostname = socket.gethostname()
		self.ip = socket.gethostbyname(self.hostname)

	def bind_socket(self):
		try:
			self.socket.bind(self.address)
		except socket.error as e:
			print(f"Bind failed, {e[0]}: {e[1]}")
			sys.exit(130)

	def listen_socket(self):
		self.socket.listen(10)
		print(f"Listenning on {self.hostname}, {self.ip}:{self.address[1]}")

	def accept_connection(self):
		while 0x42:
			self.conn = None
			self.conn_addr = None
			try:
				self.conn, self.conn_addr = self.socket.accept()
			except TimeoutError as e:
				print(f"Timeout: {e}")

			if self.conn_addr is not None:
				print(
					 "Connection received from "
					f"{self.conn_addr[0]}:{self.conn_addr[1]}"
					# f"{self.conn_addr[0]}"
				)
				break

	def send(self, part):
		byte = None
		if type(part) == int:
			byte = part.to_bytes()

		self.conn.send(byte)

	def send_address(self, addr):
		self.send(addr >> 8)
		self.send(addr & 0xff)

	def send_program(self, byte, start = 0, direction = 1):
		i = 0
		end = start + (direction * len(byte))
		for addr in range(start, end, direction):
			self.send_address(addr)
			self.send(byte[i])
			print(f"{addr:#06x}", end="")
			print(f": {byte[i]:#04x}")
			i += 1

	def close(self):
		if self.conn is not None:
			self.conn.close()
			self.conn = None
			print("Closed connection")
		if self.socket is not None:
			self.socket.close()
			self.socket = None
			print("Closed socket")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("file needed")
		sys.exit(130)

	# compiler = Compiler()
	# compiler.open(sys.argv[1])
	# compiler.compile()

	# xxd(compiler.compiled)

	# tcp_bridge = TCPBridge("", 4444)
	# tcp_bridge.accept_connection()
	# tcp_bridge.send_program(compiler.compiled, 0x0100)
	# tcp_bridge.close()


	tcp_bridge = TCPBridge("", 4444)
	tcp_bridge.accept_connection()

	for byte in [0x01, 0x02, 0x03, 0X04, 0X05, 0X06]:
		tcp_bridge.send(byte)

	tcp_bridge.close()
