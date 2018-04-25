import random
import string
import backEndRapBotv1

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, totalLines=8, syllPerLine=(7,9), seedWord='bat', randomness=0.7:
    	output = myRapBot.generateRap(totalLines, syllPerLine, seedWord, randomness)
        return output


if __name__ == '__main__':
	myRapBot = RapBot()
    cherrypy.quickstart(StringGenerator())
