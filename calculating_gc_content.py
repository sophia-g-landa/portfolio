#!/usr/bin/env python3

#Calculating CG content

#Input sequence
sequence = "ACTGATCGATTACGTATAGTATTTGCTATCATACATATATATCGATGCGTTCAT"

#Counting G & C nucleotides
g_count = sequence.count('G')
c_count = sequence.count('C')
t_count = sequence.count('T')
a_count = sequence.count('A')
#Calculating length of the sequence
sequence_length = len(sequence)
#Printing nucleotide values and sequence length
print("G count is: {0}\nC count is: {1}\nA count is: {2}\nT count is: {3}\nTotal sequence lenght: {4}".format(g_count, c_count, a_count, t_count, sequence_length))

print("The GC content is: " + str(((g_count + c_count)/sequence_length)*100) + "%")
print("The AT concent is: " + str(((a_count + t_count)/sequence_length)*100) + "%")