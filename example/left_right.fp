:PreLoopRight
MOV	AL	0x80

:LoopRight
SHR	AL	0x01
JPZ	:PreLoopLeft
JMP	:LoopRight

:PreLoopLeft
MOV	AL	0x01

:LoopLeft
SHL	AL	0x01
JPZ	:PreLoopRight
JMP	:LoopLeft
