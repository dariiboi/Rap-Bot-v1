from random import randint
import pickle
import sys
import random
import pprint
import operator
import sys,codecs,os,subprocess
import pprint
import re
#SETTINGS#
inputFileName =  "revTriChainBig.p"
rhymeInputFileName =  "rhymesBig.p"
phonemeInputFileName =  "phonemesBig.p"
maxlines = 10 #How many lines should the program write?
maxwords = 15#What's the maximum amount of words in a line before it cuts off
ChanceOfMostRealisticChain = 0#this is how likely you want the program to run the maximum likeliness generation method rather than the weighted random generation method
SeedWordMethod = 0 #0 is completely random String seed tuple, and 1 is a weighted random seed tuple
#SETTINGS#
startTuple = ("#","dick")
dict1 = pickle.load( open(inputFileName, "rb" ) )
rhymeDict = pickle.load( open(rhymeInputFileName, "rb" ) )
phonemeDict = pickle.load( open(phonemeInputFileName, "rb" ) )
ipaVowels=['i','u','ɔ','a','i','ɪ','e','ɛ','æ','a','ə','ɑ','ɒ','ɔ','ʌ','o','ʊ','u','y','ʏ','ø','œ','ɐ','ɜ','ɞ','ɘ','ɵ','ʉ','ɨ','ɤ','ɯ']
w1 = "$"
w2 = "#"
firstLine = 1 #1 is true, 0 is false
startWords = []
startDict = {}
bigrams = list(dict1.keys())
initSeed = 1
#print (phonemeDict[])
#where the rhymes happen
def rhymeTime(previousWord):
	previousPhoneme = phonemeDict[previousWord[1]]
	#print (previousPhoneme)	#derive the sound at the end of the previous 
	nextWord = random.choice(rhymeDict[previousPhoneme])	#choose a rhyming word
	nextTuple = ('#',nextWord)
	return nextTuple
def startRhyme(startPhoneme):
	nextWord = random.choice(rhymeDict[startPhoneme])	#choose a rhyming word
	nextTuple = ('#',nextWord)
	return nextTuple
def espeak2ipa(token):	#rhyming function
	CMD='speak -q --ipa '+token
	#print CMD
	try:
		phoneme = subprocess.check_output(CMD.split()).strip()
		uniCode = phoneme.decode('utf-8')
		uniCode = re.sub("ː","",uniCode)
		uniCode = re.sub("ˈ","",uniCode)
		uniCode = re.sub("ˌ","",uniCode)

		if uniCode[-1:] in ipaVowels:	#if the last sound is a vowel
			if len(uniCode) == 2:	#if the word has only 2 sounds, return the final one
				uniCode = uniCode[-1:]
			uniCode = uniCode[-2:]	#select the final 1 phonemes for the dictionary	
		else:	#if the  last sound is a consonant
			uniCode = uniCode[-3:]	#select the final 3 phonemes for the dictionary
		return uniCode
	except OSError:
		return None

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

output = []
for i in range(maxlines):
	j = 0
	#if i % 2:
	#	firstLine = 1
	if firstLine == 1:
		#output.append(inputWord[1])
		#startPhoneme = espeak2ipa(inputWord[1])
		output.append(startTuple[1])		#startTuple = startRhyme(startPhoneme)`#non functional
		prevTuple=startTuple
	else:
		prevTuple=nextTuple
		output.append(nextTuple[1])
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
	nextTuple = rhymeTime(startTuple)
	firstLine = 0 
	#print (nextTuple)
	#print (firstLine)
	output.pop()
	print(' '.join(reversed(output)))
	output = []

	


