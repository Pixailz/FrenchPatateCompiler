:Init
LD      A       0x00

:LoopUp
ADD     A       1
JPC     :LoopDown
OUTST   A
JMP     :LoopUp

:LoopDown
SUB     A       1
OUTST   A
JPZ     :LoopUp
JMP     :LoopDown
