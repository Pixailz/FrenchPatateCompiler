:PreLoopRight
LD      A       0x80

:LoopRight
SHR     A       0x01
JPZ     :PreLoopLeft
OUTST   A
JMP     :LoopRight

:PreLoopLeft
LD      A       0x01

:LoopLeft
SHL     A       0x01
JPZ     :PreLoopRight
OUTST   A
JMP     :LoopLeft
