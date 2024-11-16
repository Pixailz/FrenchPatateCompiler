LD      A   0x7f
LD      B   0x02
OUTR   
JPS     :Mult
OUTST   A
HLT

:Mult
SUB     A   0x00
JPZ     :End
SUB     B   0x00
JPZ     :EndZero
ST      A   0x00

:MultLoop
ADDR    A   0x00
JPC     :EndZero
SUB     B   0x01
JPZ     :End
JMP     :MultLoop

:EndZero
LD      A   0x00
:End
RTS
