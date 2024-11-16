:Init
STI     0x00    0x00
STI     0x01    0x01

:Loop
LDI     A       0x00
ADDR    A       0x01
JPC     :EndLoop
# Output to Stack and REG
OUTST   A
LDI     B       0x01
ST      B       0x00
ST      A       0x01
JMP     :Loop

:EndLoop
JMP     :Init