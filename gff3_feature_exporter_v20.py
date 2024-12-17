#!/usr/bin/env python3

'''
Author: Sophia Landaeta

Script is written to parse command line arguments, store them as variables, and use the variables to extract feature information and coordinates for the given attribute. The program will then search the sequence information using the chromosome and start/end positions extracted for the attribute to return the section of the FASTA sequence that matches the feature. 

References used while writing this program are listed by section as notes at the bottom of the script. 
'''

#Section 1: Module import, creating the parser with arguments, creating empty variables
import argparse #for parsing arguments from command line
import re #using a regex pattern to search for correct attribute and value

#creating the parser for command-line arguments using argparse module
parser = argparse.ArgumentParser(description='Parse through input command line arguments to select to search  GFF3 features and extract related FASTA sequence. Argument inputs are case sensitive', add_help=True)
#adding the parsing arguments for source file, feature type, attribute key, and attribute value
parser.add_argument('--source_gff', help='Path to GFF3 source file', required=True) #adding the source file argument. Required for using command line arguments parsing
parser.add_argument('--type', help='Specifying feature type, corresponding to column 3 in feature table') #adding feature type argument to filer features data
parser.add_argument('--attribute', help='Specifying the unique attribute key, corresponding to gene ID annotation in column 9 in feature table.')#adding attribute argument to specify attribute key
parser.add_argument('--value', help='Attribute value associated with attribute key, from column 9 in feature table')#adding attribute value to specify the attribute value being searched

#gather data from command line arguments, and store in args list
args = parser.parse_args() 

#assign arg values to variables 
gff3_file = args.source_gff
feature_type = args.type
feature_attribute = args.attribute
attribute_value = args.value

#Section 2: Parsing through the lines of source file to extract sequence and feature data 
#create feature counts, outside of loop
comment_lines = 0
data_lines = 0
fasta_lines = 0
in_fasta_section = False
#create empty variables for extracted data
fasta_sequences = {}#dictionary for fasta sequences
features_data = []#list for feature data
output_sequence= str()#string variable for the output sequence
#Open the gff3 file and create a for loop to iterate each line
for line in open(gff3_file):
    line = line.rstrip()#removing the new line special character(\n) at the end of each file line
    #parsing through the FASTA sequence region
    if in_fasta_section == True:
            if line.startswith('>'):#if the line is a header
                header = line[1:]#storing the header
                fasta_sequences[header] = ""#adding a new dictionary item to fasta_sequences using the header value as its key. this is creating a new entry into the dictionary for each chromosome using the chromosome value as the key
            elif header:
                 fasta_sequences[header] += line #adding the sequence lines to its dictionary entry, assigned to its specific chromosome key
            fasta_lines += 1#counting total fasta_lines parsed
    #defining that the FASTA sequence region starts with the '##FASTA' marker line
    elif line.startswith('##FASTA'):
        in_fasta_section = True
    #parsing through and counting comment lines
    elif line.startswith('#'):
        comment_lines += 1 #adds 1 to comment line counter for each comment
    else:#all other remaining lines. Should only be feature table left, as tab-delimited data in 9 columns
        columns = line.split('\t')#splitting the columns by special characted for tab
        #here we start adding conditions to filter which feature table data lines will be stored and used for final output. 
        if len(columns) == 9 and columns[2] == feature_type:#length of columns must be 9 to match gff3 format, as specified in question instructions. Furhter filtering to only those lines whose column 3 matches the feature_type that was extracted from input arguments
            notes = columns[8]#extracts column 9 as a string of annotation/feature notes. 
            attributes = notes.split(';')#splits the notes string by the semicolon(;), splitting the string to each individual attribute in column 9 of gff3 formatted data 
            for attribute in attributes:#for each individual attribute in the attributes list
                match = re.search(f'{feature_attribute}=([^;]+)', attribute)#matching to search each attribute against the formatted regex pattern with the included feature_attribute variable
                if match:#If a match is found
                    attribute_match = match.group(1)#the match is stored as attribute_match variable

                    if attribute_match == attribute_value:#attribute match variable is compared to attribute_value stored from argparse
                        feature = {#creates a feature with the feature data columns if the attribute_match == attribute_value. Feature column values specified by GFF3 format
                            'chromosome': columns[0],
                            'feature_type': columns[2],
                            'sequence_start':  columns[3],
                            'sequence_end': columns[4],
                            'strand': columns[6],
                            'annotation': columns[8]}
                        data_lines += 1 #Counting the number of queries matching the arguments given
                        #adds unique features to the features_data list
                        if feature not in features_data:
                            features_data.append(feature)

#Error messages acknowledging no matches or multiple matches
if data_lines == 0:#prints if no attribute matches the specified value
    print("\nNo attributes matched the specified attribute value {0}:{1}:{2}\n".format(feature_type, feature_attribute, attribute_value))

elif data_lines > 1:#Error message to indicate multiple matches to the attribute
    print("\nWARNING - Multiple features found to match {0}={1}\nOnly first match extracted\nPlease try again with a unique identified. Check specified 'type' or try ID attribute\n".format(feature_attribute, attribute_value))

#Section 3: Extracting feature data
if data_lines >= 1:#If data features were found
    for feature in features_data:#for each feature extracted from the columns and saved to the features_data list
        #assigning variables values from the list to build the output message
        chromosome = feature['chromosome']
        strand = feature['strand']
        #specifying the start and end positions, ensuring they are integers
        start_position = int(feature['sequence_start'])
        end_position = int(feature['sequence_end'])

    #If the extrcted chromosome value matches a key in the fasta_sequences dictionary that is storing the individual chromosome sequences
    if chromosome in fasta_sequences:
        #isolating the desired chromosome from the dictionary
        search_sequence = fasta_sequences[chromosome]
        #extracting the output sequence from the chromosome using the positions from the feature table and converting to zero-based numbering
        output_sequence = search_sequence[start_position-1:end_position]

    #Printing the desired output message!!!! I've chosen to create white space in my outputs to create space and visibility for the output sequence
    #printing the header to include feature type, attribute key, and attribute value
    print("\n>{0}:{1}:{2}".format(feature_type, feature_attribute, attribute_value))
    #printing the output sequence
    print(output_sequence)

    #Section 4: Special instructions for the negative strand genes
    if strand == "-":
        complement_sequence = str()
        def reverse_complement(sequence):
        # Complement dictionary for each nucleotide
            complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        
        # Build the reverse complement
            reverse_complement = ''.join(complement[nucleotide] for nucleotide in reversed(sequence))
            return reverse_complement
        #Applying the reverse_complement function to the output sequence, so - strand features also get a reverse complement output
        complement_sequence = reverse_complement(output_sequence)
        print("\nWARNING: This feature is on the '-' strand. The reversed complement of the extracted FASTA sequence is:\n{0}\n".format(complement_sequence))
        
#References
'''
General:
'Python for Biologists' by Martin Jones(https://pythonforbiologists.com)
'Advanced Python for Biologists' by Martin Jones(https://pythonforbiologists.com)
'Python for Everybody - Exploring Data Using Python 3' by Charles R. Severance (https://www.py4e.com/book)
'Python Cheat Sheet' by xys (https://cheatography.com/xys/cheat-sheets/python/)
'410.634 Lecture Slides - Module 8: Topic: Python (and what about Perl?)' by Joshua Orvis
'410.634 Lecture Slides - Module 8: Topic: How scripting works' by Joshua Orvis
'410.634 Lecture Slides - Module 8: Understanding the shebang line' by unkown
'410.634 Lecture Slides - Module 9: Topic: Lists, iterations, files, and functions' by Joshua Orvis
'410.634 Class Handout File - Context-based file parsing pattern' by Joshua Orvis
'410.634 Lecture Slides - Module 10: Topic: Conditionals and regular expressions' by Joshua Orvis
'410.634 Lecture Slides - Module 11: Topic: Dictionaries, files, programs, and user input' by Joshua Orvis
'410.634 Lecture Slides - Module 13: Topic: Object-oriented programming in Python' by Joshua Orvis
'410.634 Lecture Slides - Module 14: Topics: Common file formats and parsing examples' by Joshua Orvis
'PEP 8 -- Style Guide for Python' by Guido van Rossum, Barry Warsaw, and Nick Coghlan (https://legacy.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements)
Section 1:
'argparse - Parser for command-line options, arguments and subcommands' Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/library/argparse.html)
'Argparse Tutorial' by Tshepang Mbambo at Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/howto/argparse.html#argparse-tutorial)
Section 2: 
'Generic Feature Format Version 3 (GFF3)' by Lincoln Stein - The-Sequence-Ontology/Specifications (http://www.sequenceontology.org/gff3.shtml)
're — Regular expression operations' Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/library/re.html?utm_source=chatgpt.com)
'Regular Expressions HOWTO' by A.M. Kuchling at Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/howto/regex.html?utm_source=chatgpt.com)
'2. Lexical analysis' at Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/reference/lexical_analysis.html#grammar-token-stringprefix)
'2.4.3. f-strings' in 2. Lexical analysis at Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals)
Section 3:
'7. Input and Output' at Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/tutorial/inputoutput.html)
'string - Common string operations' at Python 3.13.1 Documentation - The Python Standard Library (https://docs.python.org/3/library/string.html)
'How To Index and Slice Strings in Python?' at GeeksforGeeks.org (https://www.geeksforgeeks.org/how-to-index-and-slice-strings-in-python/)
Section 4: 
'SGL_exam2_q2.py' 410.634 Exam 2 Question 2 python program submission by Sophia L. Landaeta 
'What is the fastest way to get the reverse complement of a DNA sequence in python?' at bioinformatics.stackexchange.com (https://bioinformatics.stackexchange.com/questions/3583/what-is-the-fastest-way-to-get-the-reverse-complement-of-a-dna-sequence-in-pytho)
'Reverse complement of DNA strand using Python' at GeeksforGeeks.org (https://www.geeksforgeeks.org/reverse-complement-of-dna-strand-using-python/)
'Reverse complement of DNA strand using Python' at stackoverflow (https://stackoverflow.com/questions/25188968/reverse-complement-of-dna-strand-using-python)
'Finding the reverse complement in python' at thecodingbiologist.com (https://thecodingbiologist.com/posts/finding-the-reverse-complement-in-python)
'''