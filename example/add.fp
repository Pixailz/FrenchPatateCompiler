INP     A
INP     B
JPS     :AddPrint
HLT

:AddPrint
OUTST   A
OUTST   B
ST      B   0x00
ADDR    A   0x00
OUTST   A
OUTR
RTS