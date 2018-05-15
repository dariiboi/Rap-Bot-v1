import random
import string
from backEndRapBotv1 import RapBot
import json
import cherrypy


class StringGenerator(object):
	@cherrypy.expose
	def index(self):
		return "Hello world!"

	@cherrypy.expose
	def generate(self, SeedWordMethod = 1, maxLines = 8, rhymeScheme = 2, syllableRange = 9, ChanceOfMostRealisticChain = 0.7, seedWord = 'boy'):
		lines , errorVal = myRapBot.generate(int(SeedWordMethod), int(maxLines), int(rhymeScheme), (int(syllableRange),int(syllableRange)+1), float(ChanceOfMostRealisticChain), seedWord)
		print(errorVal)
		response = {"error" : errorVal,
					"output" : lines}
		#splitOutput = "<br/>".join(output)
		return json.dumps(response)


if __name__ == '__main__':
	myRapBot = RapBot()
	cherrypy.quickstart(StringGenerator())
