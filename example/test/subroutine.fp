MOV	AL	0x01
MOV	BL	0x02
## JPS	(A)
JPS	:add_al_bl
MOV RCX	0xfe7f
HLT

:add_al_bl
ADD	AL	BL
## RTS
RTS
