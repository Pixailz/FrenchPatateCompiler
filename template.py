from	compiler	import Compiler
from	tcp_bridge	import TCPBridge

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("arg(s) needed")
		sys.exit(130)

	compiler = Compiler()
	compiler.open(sys.argv[1])
	compiler.compile()

	xxd(compiler.compiled)

	tcp_bridge = TCPBridge("", 4444)
	tcp_bridge.accept_connection()
	tcp_bridge.send_program(compiler.compiled)

	# tcp_bridge.send_program([0X01, 0x02, 0x03, 0x04, 0x05, 0x06])
	# tcp_bridge.send_program([0X00] * 0x20)
	# for byte in [0x01, 0x02, 0x03, 0X04, 0X05, 0X06]:
	# 	tcp_bridge.send(byte)

	tcp_bridge.close()
