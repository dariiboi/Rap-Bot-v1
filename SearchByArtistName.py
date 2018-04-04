
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

path = '/Users/darius/Downloads/lyricsModesmaller'
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