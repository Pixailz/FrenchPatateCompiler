#INP     A
LD      A  0x01
JPS     :Fibo
OUTST   A
HLT

:Fibo
LD      B   0x00

:FiboLoop
SUB     A   0x00
JPZ     :FiboZero
SUB     A   0x01
JPZ     :FiboOne

JPS     :FiboLoop

SUB     A   0x01
JPS     :FiboLoop
POP     B
LDI     B   0x00
ADDR    A   0x00 
RTS

:FiboZero
RTS

:FiboOne
LD      A   0x01
RTS
