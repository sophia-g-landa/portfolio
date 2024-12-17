#!usr/bin/env python3

#Splicing out introns, part 2
genomic_sequence = 'ATCGATCGATCGATCGACTGACTAGTCATAGCTATGCATGTAGCTACTCGATCGATCGATCGATCGATCGATCGATCGATCGATCATGCTATCATCGATCGATATCGATGCATCGACTACTAT'

#Functions from part 1, defining the exons 
#Specify exon 1 and exon 2 based on given character position
exon1 = genomic_sequence[0:63]
exon2 = genomic_sequence[90:]

#Calculating the total length of the genomic sequence, and of the individual exons
sequence_length = len(genomic_sequence)
exon1_length = len(exon1)
exon2_length = len(exon2)

#Printing the output of calculating the percentage of coding dna in the genomic sequence using the exon lengths and sequence length
print("The genomic sequence is " + str(((exon1_length + exon2_length)/sequence_length)*100) + "% coding.")