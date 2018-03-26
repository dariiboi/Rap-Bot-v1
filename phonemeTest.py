import sys,codecs,os,subprocess
import pprint
import re
# -*- coding: <utf-8> -*-

def espeak2ipa(token):
	CMD='speak -q --ipa '+token
	#print CMD
	try:
		phoneme = subprocess.check_output(CMD.split()).strip()
		return phoneme
	except OSError:
		return None

rawBytes=espeak2ipa('boy')
uniCode=rawBytes.decode('utf-8')
uniCode = re.sub("ː","",uniCode)
uniCode = re.sub("ˈ","",uniCode)
uniCode = re.sub("ˌ","",uniCode)
#uniCode = u'rawBytes'
#decode('utf-8')
print(uniCode)
