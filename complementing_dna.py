#!/usr/bin/env python3

#Complementing DNA 
sequence = "ACTGATCGATTACGTATAGTATTTGCTATCATACATATATATCGATGCGTTCAT"

#Manually replace the nucleotides for their complement, using lowercase to differentiate new from old
sequence1 = sequence.replace('A', 't')#complementing adenine
sequence2 = sequence1.replace('T', 'a')#complementing thymine
sequence3 = sequence2.replace('G', 'c')#complementing guanine
sequence4 = sequence3.replace('C', 'g')#complementing cytosine

#Convert to uppercase and print the new complement sequence
final_sequence = sequence4.upper()

print("The complement to sequence {0} is:\n{1}".format(sequence, final_sequence))