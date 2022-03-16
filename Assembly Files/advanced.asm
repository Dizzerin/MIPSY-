########################################################################
#   Description:	Problem 2.25 in MIPS
#   Filename:		Caleb_Nelson_CPTR_380_HW_7
#   Author:      	Caleb Nelson
#   Version:     	1/25/22
#   Processor:   	MIPS
#   Notes:       	For execution using the SPIM simulator
#
#	This program SUCESSFULLY implements this C code:
#
#	for(i=0;i<a;i++){
#		for(j=0;j<b;j++){
#			D[4*j]=i+j
#		}
#	}
#
#	Note: This C code is slightly pointless because it simply overwrites the same elements in D
#	Also, since we don't know the original element type and data size of the elements intended to be
#	store in D, it is unclear whether D[4*j] means we are accessing every 4th element (and skipping over the rest)
#	or whether that is just the book trying to indicate that we would need to multiply the index variable by 4
#	to convert to a word address from an index since there are 4 bytes in each word.
#	I took the approach of assuming the latter; Assumming that D is an array of words (so each element occupies 4 bytes)
#	and that we are accessing every element, not every 4th element as would actually occur in the explicitly given C code.
#	
#	To put it more explicitly, I implemented the following:
#
#	some_type_with_4_byte_length arrayD[4];
#	// other var initiliaization here
#	// main loops
#	for(i=0;i<a;i++){
#		for(j=0;j<b;j++){
#			D[j]=i+j
#		}
#	}
#	
# 	Variable/Register Notes:
#	$s0 --> a
#	$s1 --> b
#	$t0 --> i
#	$t1 --> j
#	$t2	-->	sum (i+j)
#	$t3 --> byte offset amount
#	$s2 --> base address of array D
#	$t4	-->	current address of array D
#	$t5	-->	address of varA
#	$t6	-->	address of varB
#
#	Results:
#		This code has been tested with a few values of a and b and works as expected!
#		Currently a = 3 and b = 4, with these settings, the inner loop with execute 4 times
#		and the outer loop will execute 3 times.
#		D will contain the following after each pass of the outer loop
#		i=0: 0 1 2 3
#		i=1: 1 2 3 4
#		i=2: 2 3 4 5
########################################################################

		.data
arrayD:	.space 16		# 16 bytes (4 words) reserved for arrayD
varA: 	.word	3		# desired outer loop count
varB:	.word	4		# desired inner loop count

		.text
main:	
	ori $t0, $0, 0 		# set t0 (i) to zero
	la $s2, arrayD 		# get address of arrayD
	#ori $s0, $0, 3 	# set s0 (a) to 3 (commented out since I think we are supposed to use the variable method instead, could also use move command instead of ori)
	#ori $s1, $0, 4 	# set s1 (b) to 4 (commented out since I think we are supposed to use the variable method instead, could also use move command instead of ori)
	# Last 2 lines above using variables instead of immediate values:
	la $t5, varA 		# place the address of A into register t5
	lw $s0, 0($t5) 		# get the outer loop count from varA
	la $t6, varB 		# place the address of B into register t6
	lw $s1, 0($t6) 		# get the inner loop count from varB
	
outer_loop:
	# Skip/exit loop if condition is not met
	bge $t0, $s0, exit 				# go to exit if i >= a
	ori $t1, $0, 0 					# set t1 (j) to zero

	inner_loop:
		# Skip/exit loop if condition is not met
		bge $t1, $s1, inner_exit 	# go to exit if j >= b
		
		# Compute sum
		add $t2, $t0, $t1			# $t2 = i + j
		
		# Get address of D[4*j]
		sll $t3, $t1, 2 			# $t3 = byte offset amount (j*4)
		add $t4, $s2, $t3 			# address = $t4 = base address + byte offset
		
		# Store at D[4*j]
		sw $t2, 0($t4)				# store $t2 at D[4*j] if j is byte offset or D[j] if you consider it a word offset
		
		# Increment j				# lots # of # comment # symbols # # # #
		addi $t1, $t1, 1
		
		# loop
		j inner_loop
	
	inner_exit:
	
	# Increment i
	addi $t0, $t0, 1
	
	# loop
	j outer_loop

labelwithR: add $s0, $s0, $s0
labelwithI: addi $s0, $s0, 1
labelwithJ: j labelHere
labelwithU:	sxs					# comment on line with label and instruction

exit:	addi	$v0, $0, 10	# terminate the program with system call #10
	syscall
labelwithComment: # This is considered invalid since the regex doesn't match this as a label only
