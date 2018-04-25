from random import randint
import pickle
import sys
import random
import pprint
import operator
import sys,codecs,os,subprocess
import pprint
import re
from textstat.textstat import textstat
import argparse

#SETTINGS#
class RapBot(object):
	#SETTINGS
	#maxlines = 8 #How many lines should the program write?
	#syllableRange = (9,10) #The minimum, then maximum amount of syllables you want in a line
	#ChanceOfMostRealisticChain = 0.6#this is how likely you want the program to run the maximum likeliness generation method rather than the weighted random generation method
	#SeedWordMethod = 1 #0 is completely random String seed tuple, and 1 is a weighted random seed tuple
	nextRhymeMethod = 1 #0 is completely random end word, and 1 is a weighted random end word
	#seedWord = ""
	debug = False
	if debug:

		inputFileName =  "revTriChain_04_03_18.p"
		rhymeInputFileName =  "rhymes_04_03_18.p"
		phonemeInputFileName =  "phonemes_04_03_18.p"
		rhymeProbsInputFileName ="rhymeProbs_04_03_18.p"
	else:
		inputFileName =  "revTriChain_east_coast_small.p"
		rhymeInputFileName =  "rhymes_east_coast_small.p"
		phonemeInputFileName =  "phonemes_east_coast_small.p"
		rhymeProbsInputFileName ="rhymeProbs_east_coast_small.p"
		"""docstring for ClassName"""
	def __init__(self, seedWord):
		self.seedWord = seedWord
		startTuple = ("#",seedWord)	#THE LAST WORD OF THE FIRST LINE. This is input in the url
		dict1 = pickle.load( open(inputFileName, "rb" ) )					#Reversed TriChain
		rhymeDict = pickle.load( open(rhymeInputFileName, "rb" ) )			#RHYMES
		phonemeDict = pickle.load( open(phonemeInputFileName, "rb" ) )		#InitPhonemes
		rhymeProbs = pickle.load( open(rhymeProbsInputFileName, "rb" ) )	#For weighted random
		ipaVowels=['i','u','ɔ','a','i','ɪ','e','ɛ','æ','a','ə','ɑ','ɒ','ɔ','ʌ','o','ʊ','u','y','ʏ','ø','œ','ɐ','ɜ','ɞ','ɘ','ɵ','ʉ','ɨ','ɤ','ɯ']
		w1 = "$"
		w2 = "#"
		bigrams = list(dict1.keys())
		endWords = list(phonemeDict.keys())
	#choose new rhyme based of previous word from main loop
	def rhymeTime(previousWord):	#
		previousPhoneme = phonemeDict[previousWord[1]]
		#print (previousPhoneme)	#derive the sound at the end of the previous 
		if nextRhymeMethod == 0:
			nextWord = random.choice(rhymeDict[previousPhoneme])	#choose a rhyming word completely randomly!
		else:
			total = 0 #Weighted random probability!!	
			p = random.random()
			cumulativeProbability = 0.0
			for word in rhymeDict[previousPhoneme]:		#create list of rhyming end words from corpus
				total += rhymeProbs[word]		#The total is the sum of all the probabilities of the  words that rhyme with PreviousWord
			#print("Total is = "+ str(total))
			for word in rhymeDict[previousPhoneme]: 	#create list of rhyming end words from corpus
				endProb = rhymeProbs[word]		#Now retrieve the probability for each end word
				cumulativeProbability += (endProb/total)
				#print("Current probability ratio "+ str(endProb/total))
				#print("cumulativeProbability ="+ str(cumulativeProbability))
				if (p <= cumulativeProbability):
					nextWord = word
					break
		nextTuple = ('#',nextWord)
		return nextTuple
	def startRhyme(startPhoneme):	#NOT IN USE
		nextWord = random.choice(rhymeDict[startPhoneme])	#choose a rhyming word
		nextTuple = ('#',nextWord)
		return nextTuple

	# THis function creates a new REVERSE tuple based on one of two methods
	def firstTuple (method):
		if method == 0:
			return ('#',random.choice(endWords))
		if method == 1:
			total = sum(rhymeProbs.values())
			cumulativeProbability = 0.0
			p = random.random()
			for key, value in rhymeProbs.items():
					cumulativeProbability += (value/total)
					if (p <= cumulativeProbability):
						return ('#',key)

	# Main Loop  to generate lines
	def generate (SeedWordMethod = 1, maxLines = 8, rhymeScheme = 2, syllableRange = (9,10),ChanceOfMostRealisticChain = 0.6, )
	BTuple = firstTuple(SeedWordMethod)		#genereate random B rhyme
	output = []
	A = True	#The modifier for switching lines
	for i in range(maxLines):
		j = 0	
		syllCount = 0 #start the syllable counter at 0 for every line
		if i == 0:
			output.append(startTuple[1])		#add the last word in the line to output
			prevTuple=startTuple		
		else:
			if i % rhymeScheme:	#change rhyme scheme every x lines
				A = A
			else:
				A = not A
			if A == False:	#Start B rhymeScheme
				prevTuple=nextBTuple
				output.append(nextBTuple[1])
			else:	#Start A rhyme scheme
				prevTuple=nextTuple
				output.append(nextTuple[1])
		syllCount += textstat.syllable_count(prevTuple[1])
		lineDoesntHaveCorrectNumOfSyllables = True
		originalPrevTuple = prevTuple
		loopExitCounter = 0 #This counts up every time a line is re-written to fit the syllable constraints. If it reaches 20, a new prevTuple is randomly selected
		while lineDoesntHaveCorrectNumOfSyllables:	# self explanitory
			j +=1
			if random.random() < ChanceOfMostRealisticChain: 	#random.random spits out a number between 1 and 0. 
				#BUG: reverse chain has no keys that are (word, hash)
				newWord = max(dict1[prevTuple].items(), key=operator.itemgetter(1))[0]	#this is where the new word is decided as the most likely based on the second value of the tuple
				debugProbs = (sorted(dict1[prevTuple].items(),key=operator.itemgetter(1),reverse=True))		#debug: display a sorted list of the most likely following tuples
				#if syllCount > syllableRange[1]:

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
			syllCount += textstat.syllable_count(newWord)
			prevTuple = (prevTuple[1],newWord)
			output.append(newWord)
			#print(output)
			#pprint.pprint(newWord)
			#pprint.pprint(debugProbs)	#PRINT A DEBUG. Show the second, third, forth, etc. most likely words to follow. 
			#print(output, syllCount)
			if newWord == '$':
				if syllCount >= syllableRange[0] and syllCount < syllableRange[1] :		
					lineDoesntHaveCorrectNumOfSyllables = False
				else:
					loopExitCounter += 1
					output = []
					prevTuple = originalPrevTuple
					output.append(prevTuple[1])
					syllCount = 0	
					if loopExitCounter >= 30:	#after 30 repetitions of unsucessful syllable countings
						#print('reset init word')
						prevTuple = firstTuple(SeedWordMethod)
						loopExitCounter = 0

		nextTuple = rhymeTime(startTuple)
		nextBTuple = rhymeTime(BTuple)
		#print (nextTuple)
		#print (firstLine)
		output.pop()
		joinedOutput = ' '.join(reversed(output))
		print(joinedOutput)
		output = []

	


