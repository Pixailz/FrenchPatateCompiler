$PATTERN 0x00
LD A 0x00
:LOOP
LDE A $PATTERN
ADD A 0x01
JPC :END
JMP :LOOP
:END
HLT