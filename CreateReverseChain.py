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
import codecs,os,subprocess
import io
#SETTINGS#
#create corpus from certain artists, the artist's names are in 3 letter combinations, eg. KEN for kendrick Llamar
debug = False
ArtistRestriction = True #Does the code select from a list of artists, or make a chain out the the entire corpus
artistFiles = []
ipaVowels=['i','u','a','i','ɪ','e','ɛ','æ','a','ə','ɑ','ɒ','ɔ','ʌ','o','ʊ','u','y','ʏ','ø','œ','ɐ','ɜ','ɞ','ɘ','ɵ','ʉ','ɨ','ɤ','ɯ']
#regionFile = open('/Users/darius/Documents/eastCoastArtists.txt')
with io.open('/Users/darius/Documents/eastCoastArtists.txt', 'r',encoding="utf-8") as myfile:
	regionFile = myfile.read()
regionList = regionFile.split('\n')
#print (regionList)
if debug:
	path = '/Users/darius/Documents/ComSci2/project4/lyricsmode'
else:
	path = '/Users/darius/Downloads/lyricsModesmaller'
outputFileName = "triChain_04_03_18.p"
reverseOutputFileName = "revTriChain_04_03_18.p"
phonemeOutputFileName = "phonemes_04_03_18.p"	#key: word, value: phoneme
rhymeOutputFileName = "rhymes_04_03_18.p"	#key: phoneme, value: list of words
rhymeProbsFileName = "rhymeProbs_04_03_18.p"	#key: phoneme, value: list of words
inputFileName = 'artistDict1.p'
artistDict = pickle.load( open(inputFileName, "rb" ) )

#CODE#
sys.getdefaultencoding()
badcount = 0
#path = '/Users/darius/Documents/ComSci2/project4/lyricsmode'
rhymeProbs = {}
forwardDict = {}
reverseDict = {}
phonemeDict = {}
rhymeDict = {}
words = []
endWordCount = 0.0
wordCount = 0.0
#remove whitespaces, punctuation, uppercase from lists of artist names
def normalizeStrings(t):
	t = t.lower()	#ALL LOWERCASE
	t = re.sub("[\(\[].*?[\)\]]", "", t)	#NO PUNCTUATION
	t = re.sub("[éêè]",'e',t)
	t = re.sub("[^a-z0-9' \n]*", "", t)
	t = re.sub("\s+", "", t.strip())
	return(t)
#look through all artist files for artist names and choose the files that contain the artist's name
def chooseArtists(artistList):	
	for wikiName in artistList:		#look thru all of the artists in the list
		for corpusName in artistDict.keys():
			normCorpusName = normalizeStrings(corpusName)	#normalize the names of the artists in the dictionary of artistnames
			normWikiName = normalizeStrings(wikiName)	#normalize the names of the artists from my wikipedia-derived regional list
			if normWikiName in normCorpusName:	#if there's a match between the two....
				artistFiles.extend(artistDict[corpusName])	#append the list to include
	print(artistFiles)			
#take words and split them into a 3 part trigram
def generateTrigram(words):
    if len(words) < 3: #unless the line has less than 3 words tho
        return
    for i in range(len(words) - 2): 
        yield (words[i], words[i+1], words[i+2])

def generateReverseTrigram(words):
	if len(words) < 3: #unless the line has less than 3 words tho
 		return
	for i in reversed(range(2,len(words))): #between the beginning and end of the line:
		yield (words[i-2], words[i-1], words[i]) #yield the first, second, and third word
 
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
	#print (line)
	for word3, word2, word1 in generateReverseTrigram(words):
		#print(word3 +" "+ word2 +" "+ word1)
		#the first 2 words in the trigram become the tuple key
		if not word1 or not word2 or not word3 or word1 == "'" or word2 == "'" or word3 == "'": 	#is one of the keys an empty string?
			if debug:
				print(word1 + " " + word2  + " " + word3 )
			continue	#dont add it to the dictionary
		else:	
			key = (word1, word2)
			#print (key)
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
			
def final2Phonemes(token):	#rhyming function
	CMD='speak -q --ipa '+token
	#print CMD
	try:
		phoneme = subprocess.check_output(CMD.split()).strip()
		uniCode = phoneme.decode('utf-8')
		uniCode = re.sub("ː","",uniCode)
		uniCode = re.sub("ˈ","",uniCode)
		uniCode = re.sub("ˌ","",uniCode)

		if len(uniCode) == 1:	#if the word has only 1ç sound, return the final one
			uniCode = uniCode[-1:]
			#print(uniCode)
			return uniCode
		if len(uniCode) >3:
			if uniCode[-2] and uniCode[-3] in ipaVowels :	#If the second and third last phoneme are vowels, the word has a conjunction vowel like kˈəʊk (coke)
				uniCode = uniCode[-3:]	#select the final 3 phonemes for the dictionary	
				#print(uniCode)
				return uniCode	
		if uniCode[-2] in ipaVowels or uniCode[-1] in ipaVowels :	#if the last or second last sound is a vowel
			uniCode = uniCode[-2:]	#select the final 2 phonemes for the dictionary	
			#print(uniCode)
			return uniCode
		else:	#if the  last sound is a consonant
			uniCode = uniCode[-3:]	#select the final 3 phonemes for the dictionary
			#print(uniCode)
			return uniCode
	except OSError:
		return None

fileCount = 0

#look thru path for files
for filename in os.listdir(path):
	myfile = ''
	
	if ArtistRestriction == True: 
		chooseArtists(regionList)
		for file in artistFiles: #for all the files in the subdivision of artist files (eg west coast artists)
			if filename == file:	#for every file in the main folder that matches a file in the subsection of area-specific artists:
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
	t = re.sub("[éêè]",'e',t)
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
		if debug:
			print(str(fileCount))
			chainSize = sys.getsizeof(forwardDict)
			print('Chain size = ' + str(chainSize))

print("converting to probabilities")
#for every key in the main dictionary, convert the respective count into a probability.
for key in forwardDict:
	for word in forwardDict[key]:
		forwardDict[key][word] = forwardDict[key][word]/wordCount
		#print("Forward dictionary in process")
print("now reverse dict")
myCount = 0
numKeys = len(reverseDict)
for key in reverseDict:
	for prevWord in reverseDict[key]:	# for every time a word comes up as the value of reverseDIct, divide it by the word count to make the probability
		reverseDict[key][prevWord] = reverseDict[key][prevWord]/wordCount
	myCount += 1
	if key[0] == '#':			#is this a final word?
		endWordCount += 1
		#print("phoneme dictionary in process "  + key[1] + " at " + str(myCount) + " of " + str(numKeys))
		finalPhoneme = final2Phonemes(key[1])	#iteratate thru all phonemes and return them as keys to the Phoneme dictionary
		if finalPhoneme is None:
			print("Espeak failed on " + key[1])		#give the key on which espeak failed
			continue
		if key[1] in rhymeProbs:
			rhymeProbs[key[1]] += 1
		else:
			rhymeProbs[key[1]] = 1
		phonemeDict[key[1]]=finalPhoneme
		
		if finalPhoneme in rhymeDict:
			rhymeDict[finalPhoneme].append(key[1])
		else:
			rhymeDict[finalPhoneme]=[]
			rhymeDict[finalPhoneme].append(key[1])
			#print("Rhyming dictionary in process")
for rhymeKey in rhymeProbs.keys():	#for every key in the dict, divide the wordcount by the total number of end words to get a probability
	rhymeProbs[rhymeKey] = rhymeProbs[rhymeKey]/endWordCount
	
	#print(phonemeDict)
print("saving pickle.")
pickle.dump( forwardDict, open( outputFileName, "wb" ) )	
# GENERATE OUTPUT
print("saving pickle 2.")
pickle.dump( reverseDict, open( reverseOutputFileName, "wb" ) )	
# GENERATE OUTPUT
print("saving pickle 3.")
pickle.dump( phonemeDict, open( phonemeOutputFileName, "wb" ) )	
# GENERATE OUTPUT
print("saving pickle 4.")
pickle.dump( rhymeDict, open( rhymeOutputFileName, "wb" ) )	
print("saving pickle 5.")
pickle.dump( rhymeProbs, open( rhymeProbsFileName, "wb" ) )	
print("all done!")
#print(rhymeDict)
