#!/usr/bin/env python
# Simple Vigenere cipher decoder implementation in Python, using a graphical approach (as you would do in a piece of paper)
# Idea taken from the book: "The code book" by Simon Simgh
# https://bynario.com/2017-03-10-simple-Vigenere-cipher-in-python-(and-3).html
# Further reading: https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
import string

mykey="WHITE"
input_text="en un lugar de la mancha de cuyo nombre no quiero acordarme"
code_text="AU CG PQNIK HA SI FEJJPT HA JCRS JVUUVA UW JYELZH EYVZWENTM"

# Alphabet used as reference (M)
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
source = string.ascii_uppercase

# Key alphabet (K) shifted 1 position to the left
# BCDEFGHIJKLMNOPQRSTUVWXYZA
shift = 1
matrix = [ source[(i + shift) % 26] for i in range(len(source)) ]

def coder(thistext):
	ciphertext = []
	control = 0

	for x,i in enumerate(input_text.upper()):
	    if i not in source: 
	    	#If the symbol is not in our reference alphabet, we simply print it
	        ciphertext.append(i)
	        continue
	    else:
	    	#Wrap around the mykey string 
	        control = 0 if control % len(mykey) == 0 else control 
	        
	        #Calculate the position C[i] = (M[i]+K[i]) mod len(M)
	        result = (source.find(i) + matrix.index(mykey[control])) % 26
	        #Add the symbol in position "result" to be printed later
	        ciphertext.append(matrix[result])
	        control += 1
	
	return ciphertext

def decoder(thistext):
	control = 0
	plaintext = []

	for x,i in enumerate(code_text.upper()):
	    if i not in source: 
	        #If the symbol is not in our reference alphabet, we simply print it
	        plaintext.append(i)
	        continue
	    else:
	        #Wrap around the mykey string 
	        control = 0 if control % len(mykey) == 0 else control 
	   
	        #Calculate the position M[i] = (C[i]-K[i]) mod len(M)
	        result = (matrix.index(i) - matrix.index(mykey[control])) % 26

	        #Add the symbol in position "result" to be printed later
	        plaintext.append(source[result])
        	control += 1

	return plaintext

# Print results
print("Key: {0}".format(mykey))
print("\nDecode text:")
print("-> Input text: {0}".format(input_text))
print("-> Coded text: {0}".format(''.join(coder(input_text))))

# Print results
print("\nDecode text:")
print("-> Input text: {0}".format(code_text))
print("-> Decoded text: {0}".format(''.join(decoder(code_text)).lower()))

