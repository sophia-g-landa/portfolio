#!usr/bin/env python3

#Splicing out introns, part 3
genomic_sequence = 'ATCGATCGATCGATCGACTGACTAGTCATAGCTATGCATGTAGCTACTCGATCGATCGATCGATCGATCGATCGATCGATCGATCATGCTATCATCGATCGATATCGATGCATCGACTACTAT'

#Functions from part 1, defining the exons 
#Specify exon 1 and exon 2 based on given character position
exon1 = genomic_sequence[0:63]
exon2 = genomic_sequence[90:]
intron = genomic_sequence[63:90].lower()#Specify the intron positions and lowercase them

#Build and print the complete sequence again, with coding regions capitalized
print(exon1 + intron + exon2)
