#JPS     :TestADD
#JPS     :TestSUB
#JPS     :TestADDR
JPS     :TestCondition
HLT

:TestADD
LD      A       0x01
ADD     A       0x01
RTS

:TestSUB
LD      A       0x01
SUB     A       0x01
RTS

:TestADDR
STI     0x00    0x01
ADDR    A       0x00
RTS

:TestCondition
LD      A       0x01
SUB     A       0x00
JPZ     :TestConditionZero
SUB     A       0x01
JPZ     :TestConditionOne

:TestConditionZero
LD      A       0x04
RTS     

:TestConditionOne
LD      A       0x08
RTS