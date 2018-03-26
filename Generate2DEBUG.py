from random import randint
import pickle
import sys
import random
import pprint
import operator
#SETTINGS#
inputFileName =  "revTriChain1.p"
maxlines = 16 #How many lines should the program write?
maxwords = 15#What's the maximum amount of words in a line before it cuts off
ChanceOfMostRealisticChain = 0#this is how likely you want the program to run the maximum likeliness generation method rather than the weighted random generation method
SeedWordMethod = 1 #0 is completely random String seed tuple, and 1 is a weighted random seed tuple
#SETTINGS#

dict1 = pickle.load( open(inputFileName, "rb" ) )
w1 = "$"
w2 = "#"

startWords = []
startDict = {}
bigrams = list(dict1.keys())
#print(bigrams)
def sumProbs (input):
	total = 0.0
	for word in input:
		total += input[word]
	return total

for i in bigrams:
	if i[0] == '#':
		#Creating sum of all probabilities of bigrams that start with the following 
		startDict[i]= sum(dict1[i].values())
		startWords.append(i[1])
		

#pprint.pprint(startWords)
#thefile = open('checking.txt', 'w')
#for item in bigrams:
#	thefile.write("%s\n" % str(item))
#exit()

# THis function creates a new REVERSE tuple based on one of two methods
#
#
def firstTuple (method):
	global startWords
	global startDict
	if method == 0:
		return ('#',random.choice(startWords))
	if method == 1:
		total = sum(startDict.values())
		cumulativeProbability = 0.0
		p = random.random()
		for key, value in startDict.items():
				cumulativeProbability += (value/total)
				if (p <= cumulativeProbability):
					return (key)


#
# Main Loop  to generate lines
#
#
#pprint.pprint (newTuple())
output = []
for i in range(maxlines):
	prevTuple = firstTuple(SeedWordMethod)
	j = 0
	output.append(prevTuple[1])
	#print(prevTuple)
	while j < maxwords:
		j +=1
		if random.random() < ChanceOfMostRealisticChain: 	#random.random spits out a number between 1 and 0. 
			#BUG: reverse chain has no keys that are (word, hash)
			newWord = max(dict1[prevTuple].items(), key=operator.itemgetter(1))[0]	#this is where the new word is decided as the most likely based on the second value of the tuple
			debugProbs = (sorted(dict1[prevTuple].items(),key=operator.itemgetter(1),reverse=True))		#debug: display a sorted list of the most likely following tuples
		else: 
			#newWord = min(dict1[prevTuple].items(), key=operator.itemgetter(1))[0]
			total = sum(dict1[prevTuple].values()) 
			p = random.random()
			cumulativeProbability = 0.0
			for key, value in dict1[prevTuple].items():
				cumulativeProbability += (value/total)
				if (p <= cumulativeProbability):
					newWord = key
					#print(' '+ str(value/total)+ ' ')
					break

		prevTuple = (prevTuple[1],newWord)
		output.append(newWord)
		#pprint.pprint(newWord)
		#pprint.pprint(debugProbs)	#PRINT A DEBUG. Show the second, third, forth, etc. most likely words to follow. 
		if newWord == '$' :		
			break
	output.pop()
	print(' '.join(reversed(output)))
	output = []
	


