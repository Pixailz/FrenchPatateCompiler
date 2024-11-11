$BYTE   0x12
LD      A       $BYTE

:Loop
NOT     A       0x00
OUTST   A   
JMP     :Loop
