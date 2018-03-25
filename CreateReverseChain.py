from __future__ import division
import string 
import pickle
from bs4 import BeautifulSoup
import csv
import re
import os
import sys
import random
import fnmatch
import pprint
#SETTINGS#
#create corpus from certain artists, the artist's names are in 3 letter combinations, eg. KEN for kendrick Llamar
artistNames = [".ken.txt"]
path = '/Users/darius/Documents/ComSci2/project4/lyricsmode'
outputFileName = "triChainKen.p"
reverseOutputFileName = "revTriChainKen.p"
ArtistRestriction = 1 #Does the code select from a list of artists, or make a chain out the the entire corpus
#SETTINGS#


#CODE#
sys.getdefaultencoding()
badcount = 0
#path = '/Users/darius/Documents/ComSci2/project4/lyricsmode'

forwardDict = {}
reverseDict = {}
words = []
wordCount = 0.0
#take words and split them into a 3 part trigram
def generateTrigram(words):
    if len(words) < 3: #unless the line has less than 3 words tho
        return
    for i in range(len(words) - 2): 
        yield (words[i], words[i+1], words[i+2])

def generateReverseTrigram(words):
	if len(words) < 3: #unless the line has less than 3 words tho
 		return
	for i in reversed(range(2,len(words))):
		yield (words[i-2], words[i-1], words[i])
 
 #add counts to words after tuples
def count(line):
	global forwardDict
	global wordCount
	#make words from line
	words = line.split(' ')
	wordCount += len(words)
	#run the trigram maker on 1 line which returns a set of 3 words
	for word1, word2, word3 in generateTrigram(words):
		#the first 2 words in the trigram become the tuple key
		key = (word1, word2)
		if key in forwardDict:
			if word3 in forwardDict[key]:
				#add a count to the amount of times you've seen a word after a tuple
				forwardDict[key][word3] += 1.0
			else:
				#if you havent seen word 3 before add it to the dictionary
				forwardDict[key][word3] = 1.0
		else:
			#If you haven't seen a tuple before add it to the dictionary
			forwardDict[key] = {}
			forwardDict[key][word3] = 1.0

def revCount(line):
	global reverseDict
	global wordCount
	#make words from line
	words = line.split(' ')
	wordCount += len(words)
	#run the trigram maker which returns a set of 3 words
	print (line)
	for word3, word2, word1 in generateReverseTrigram(words):
		print(word3 +" "+ word2 +" "+ word1)
		#the first 2 words in the trigram become the tuple key
		key = (word1, word2)
		print (key)
		if key in reverseDict:
			if word3 in reverseDict[key]:
				#add a count to the amount of times you've seen a word after a tuple
				reverseDict[key][word3] += 1.0
			else:
				#if you havent seen word 3 before add it to the dictionary
				reverseDict[key][word3] = 1.0
		else:
			#If you haven't seen a tuple before add it to the dictionary
			reverseDict[key] = {}
			reverseDict[key][word3] = 1.0
		

fileCount = 0

#look thru path for files
for filename in os.listdir(path):
	myfile = ''
	
	if ArtistRestriction == 1: 
		for i in artistNames: #is the artist in the filename??
			if i in filename:
				myfile = path+"/"+filename	#create file path
				continue
		if myfile == '':
			continue
	else:
		myfile = path+"/"+filename	#create file path
	#print(myfile)
	pretext = ''
	t= ''
	t2= u''	
	try:
		#try to read the file and decode it into utf8 format
		f = open(myfile, 'rb')
		t2 = f.read().decode('utf8', 'ignore')
		
	except: # if that doesnt work that try to encode it into latin 1
		t2 = open(myfile, encoding="latin-1 ").read()
		print("fallback to latin 1:", sys.exc_info()[1])
		e = sys.exc_info()[0]
		print("latin file: \n"+ myfile)
	try: #take out all the nasty HTML
		soup = BeautifulSoup(t2, "html.parser")
		#take the text between the HTML tags
		pretext = soup.find_all('pre')
	except: 
		#if beautifulsoup decoder fails:
		badcount+=1
		#if all other checks fail, go here
		print("Unexpected error from soup:", sys.exc_info()[1])
	#if the .txt file is not sepererated using <pre> tags in HTML
	if len(pretext) > 0:
		for t in pretext:
			t = t.get_text()
	else:
		try:
			#in the situation that there is no HTML in the .txt, go through a more simple decoding process
			rawfile = open(myfile, encoding='latin1')
			t = rawfile.read()
		except:
			print("badfile2 :"+ myfile)
	#convert everything to lowercase
	t = t.lower()
	#take out things between the following symbols
	t = re.sub("[\(\[].*?[\)\]]", "", t)
	#make sure to only use letters and numbers n the english alphebet and number system
	t = re.sub("[^a-z0-9' \n]*", "", t)

	#print(t)
	#turn the big text chunk into lines
	lines = t.split('\n')
	lines = lines[6:] #remove first 6 lines of file which are useless
	for line in lines:
		line = ' '.join(line.split())
		#remove this text from all lines. it's not actually rap.
		line = re.sub('typist requests corrections where needed','', line)
		line = re.sub('send corrections to the typist','', line)
		line = re.sub('please send corrections to the typist','', line)
		line = re.sub('please send corrections to the typist','', line)
		#add $ sign at the beginning of a line and# sign at the end. Do this if the line has 1 or more alphanumerical characters within it
		if re.match('\w+',line):
			newline = '$ ' + line + ' #'
			count(newline) #pass clean line to the counting function
			revCount(newline)
			
	fileCount += 1
	#when building, count every 100 files
	if (fileCount % 100 == 0):
		print(str(fileCount))
		chainSize = sys.getsizeof(forwardDict)
		print('Chain size = ' + str(chainSize))

print("converting to probabilities")
#for every key in the main dictionary, convert the respective count into a probability.
for key in forwardDict:
	for word in forwardDict[key]:
		forwardDict[key][word] = forwardDict[key][word]/wordCount

for key in reverseDict:
	for word in reverseDict[key]:
		reverseDict[key][word] = reverseDict[key][word]/wordCount
	
print("saving pickle.")
pickle.dump( forwardDict, open( outputFileName, "wb" ) )	
# GENERATE OUTPUT
print("saving pickle.")
pickle.dump( reverseDict, open( reverseOutputFileName, "wb" ) )	

print("all done!")
