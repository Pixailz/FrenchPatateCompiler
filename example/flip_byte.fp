$BYTE_1 0x12
$BYTE_2 0x34

:Init
LD      A       $BYTE_1
STI     0x00    $BYTE_2

:Loop
XORR    A       0x00
ST      A       0x01
LDI     A       0x00
XORR    A       0x01
ST      A       0x00
LDI     A       0x01
XORR    A       0x00
LDI     B       0x00
OUTST   A   
OUTST   B
JMP     :Loop
