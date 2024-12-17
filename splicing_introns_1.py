#!usr/bin/env python3

#Splicing out introns, part 1
genomic_sequence = 'ATCGATCGATCGATCGACTGACTAGTCATAGCTATGCATGTAGCTACTCGATCGATCGATCGATCGATCGATCGATCGATCGATCATGCTATCATCGATCGATATCGATGCATCGACTACTAT'

#Specify exon 1 and exon 2 based on given character position
exon1 = genomic_sequence[0:63]
exon2 = genomic_sequence[90:]

#Print the coding regions
print("Exon 1: " + exon1)
print("Exon 2: " + exon2)

print("CDS: " + exon1 + exon2)
