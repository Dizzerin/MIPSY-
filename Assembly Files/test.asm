lw $t0, 1200($t1)
label1:
	add $t0, $s2, $t0
	j label1
	addiu $s1, $s2, 100
	addi $s1, $s2, -1
	bne $s0, $s1, label2
	sll $t2, $s0, 4
	j label1
	# j 2000 # TODO support this type of jump
label2:
	jr $ra
	jal label1
	bne $s0, $s1, label2