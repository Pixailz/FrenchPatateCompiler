$begin_zero = 0x05
$begin_carry = 0xf5


MOV	AL	$begin_zero

:LoopZero
SUB	AL	0x01
JPZ	:InitLoopCarry
JMP :LoopZero

:InitLoopCarry
MOV	RBX	0x0001
MOV	AL	$begin_carry

:LoopCarry
ADD AL	0x01
JPC	:End
JMP	:LoopCarry


:End
MOV	RBX	0x0003
HLT
