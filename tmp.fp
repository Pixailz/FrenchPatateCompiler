$constant	= 0x01
$address	= @0x002
$reg		= B

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