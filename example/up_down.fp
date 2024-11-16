:Init
LD      A       0x00

:LoopUp
ADD     A       1
JPC     :Up2Down
OUTST   A
OUTR
JMP     :LoopUp

:Up2Down
SUB     A       1

:LoopDown
SUB     A       1
OUTST   A
OUTR
JPZ     :LoopUp
JMP     :LoopDown
