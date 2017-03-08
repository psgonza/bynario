#!/usr/bin/env python
# Simple Vigenere cipher decoder implementation in Python, using a graphical approach (as you would do in a piece of paper)
# Idea taken from the book: "The code book" by Simon Simgh
# Further reading: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
import string

mykey="WHITE"
input_text="AU CG PQNIK HA SI FEJJPT HA JCRS JVUUVA UW JYELZH EYVZWENTM"

cleartext = []
matrix = []
encryption_tuple= []
row = 0
control = 0

# Alphabet used as reference
source = string.ascii_uppercase

#Creating the Vigenere Square. A 26x26 matrix. 
# In the example provided by the book, instead of using the regular alphabet as reference, we shift the items, so 
# so the column used as reference doesn't start in A, but in B
for row in range(len(source)):
    matrix.append([ x for i,x in enumerate(source) if i > row ])   
    for i,x in enumerate(source):
        if i <= row: matrix[row].append(x)

# Creating the tuple based on the letter and key. ie:
# ('D', 'W'), ('I', 'H'), ('V', 'I'), ('E', 'T'), ('R', 'E'), ('T', 'W'), ('T', 'H'), ('R', 'I'), ...        
# In case special characters are not considered, this is cleaner:
#   import itertools
#   text=[ x for x in input_text.upper() if x in string.ascii_letters]
#   encryption_tuple = [(x,y) for x,y in zip(text, itertools.cycle(mykey))]
for x,y in enumerate(input_text.upper()):
    control = 0 if control % len(mykey) == 0 else control
    if y in string.punctuation or y in string.whitespace:
         encryption_tuple.append((y,y))
    else:
         encryption_tuple.append((y,mykey[control]))
         control += 1
                
# Each element y in the tuple is the key in the alphabet matrix
for x,y in encryption_tuple:
    if source.find(x) == -1: 
        cleartext.append(x)
    else:
        ref_row = matrix[0].index(y)
        cleartext.append(source[matrix[ref_row].index(x)])

# Print guide
print("-> Reference:")        
print("   " + ' '.join([x for x in source]))
# Printing Vigenere square
print("-> Square:")        
for id,i in enumerate(matrix,1):
    print("{:02d} {}".format(id,' '.join(i)))
# Print results
print("-> Key: {0}".format(mykey))
print("-> Input text: {0}".format(input_text))
print("-> Output text: {0}".format(''.join(cleartext)))
