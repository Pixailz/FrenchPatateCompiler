$constant1	= 1
$constant2	= 0b10
$constant3	= 0x03
$address	= @0x0002
$reg		= AL

:label1
MOV	$reg		$address
:label2
MOV	$address	$reg
:label3
MOV $reg		$constant
:label4
MOV	$address	$constant
:label5
MOV	$reg		:label5
MOV	:label1		$constant
