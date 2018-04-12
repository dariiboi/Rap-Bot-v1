
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
ArtistRestriction = 0 
artistNames = [".txt"]
artistDict = {} #Where we can cross reference artist name and text file
path = '/Users/darius/Downloads/lyricsModesmaller'	
#look thru path for files
outputFileName = "artistDict1.p"
for filename in os.listdir(path):
	myfile = ''
	myfile = path+"/"+filename	#create file path
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
	lines = t.split('\n')	#split text file into lines
	for line in lines:
		if line.startswith('Artist:') or line.startswith('artist:'):	#find the lines where they say who the artist is
			line = re.sub('Artist:','',line)
			if 'f/' in line:
				name = line.split('f/', 1)[0]	#remove the features from the artist name
				break
			if 'feat' in line:
				name = line.split('feat', 1)[0]	#remove the features from the artist name
				break	
			else:
				name = line
				break
	if name[-1] == ' ':
		name = name[:-1]		#remove space from before artist name
	if name[0] == ' ':
		name = name[1:]		#remove space from after artist name
	if name in artistDict:
		artistDict[name].append(myfile)
	else:
		artistDict[name] = []
		artistDict[name].append(myfile)
print (artistDict)
pickle.dump( artistDict, open( outputFileName, "wb" ))	

