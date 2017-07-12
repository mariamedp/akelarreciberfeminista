# -*- coding: utf-8 -*-

# Ejemplo de uso de AkelarreBot

import os
import time
import sys
import json

from akelarrebot import AkelarreBot

###
		
# Argumentos de entrada: <fichero .json de credenciales de twitter> <fichero de listado de trolls>
try:
	credentials_filename = sys.argv[1]
	recopilacion_filename = sys.argv[2]
except IndexError:
	print('Error en la entrada: ' + sys.argv[0] + ' <fichero .json de credenciales de twitter> <fichero de listado de trolls>')
	sys.exit(1)

	
# Inicialización

tweetbot = AkelarreBot(recopilacion_filename, chainlength=4)

dirname = os.path.dirname(os.path.abspath(__file__))
book = os.path.join(dirname, u'texto_ejemplo.txt')
tweetbot.read(book)


# Log in to Twitter

with open(credentials_filename, 'r') as f:
	twitter_credentials = json.load(f)

tweetbot.twitter_login(twitter_credentials['consumer_key'], 
                       twitter_credentials['consumer_secret'], 
                       twitter_credentials['access_key'], 
                       twitter_credentials['access_secret'])


# Start autorecopilacion Thread	
hechizos = ["blublublu"]				   
tweetbot.twitter_autorecopilaciontrolls_start(hechizos)


# DO SOMETHING HERE TO ALLOW YOUR BOT TO BE ACTIVE IN THE BACKGROUND
# You could, for example, wait for a week:
secsinweek = 7 * 24 * 60 * 60
time.sleep(secsinweek)


# Use the following to stop auto-responding
# (Don't do this directly after starting it, or your bot will do nothing!)
tweetbot.twitter_autorecopilaciontrolls_stop()


