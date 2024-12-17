#!/usr/bin/env python3

#Restriction frament lengths
sequence = "ACTGATCGATTACGTATAGTAGAATTCTATCATACATATATATCGATGCGTTCAT"
EcoRI_recognition_site = 'GAATTC'
#Find the position of EcoRI restriction enzyzme recognition site
cut_site1 = sequence.find(EcoRI_recognition_site)
#Create first fragment using cut_site1 position
fragment1 = sequence[0:cut_site1+1]
#Create second fragment using cut_site1 position
fragment2 = sequence[cut_site1+1:]

#Print out restriction fragments and their lengths
print("Fragment 1: {0}".format(fragment1))
print("Fragment 1 length: " + str(len(fragment1)))
print("Fragment 2: {0}".format(fragment2))
print("Fragment 2 length: " + str(len(fragment2)))