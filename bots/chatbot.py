# -*- coding: utf-8 -*-

# Bot de ejemplo para Twitter
# Version 1.0 - Capaz de responder a otros perfiles, con autenticación segura

import os
import time
import sys
import json

from markovbot import MarkovBot

###

# Argumento de entrada: nombre del fichero .json con las credenciales de twitter
try:
	text_filename = sys.argv[1]
except IndexError:
	print('Error: falta indicar el nombre del fichero .json con las credenciales de twitter')
	sys.exit(1)

# # # # #
# INITIALISE

# Initialise a MarkovBot instance
tweetbot = MarkovBot()
# Get the current directory's path
dirname = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the book
book = os.path.join(dirname, u'texto_ejemplo.txt')
# Make your bot read the book!
tweetbot.read(book)


# # #
# TEXT GENERATION

# Generate text by using the generate_text method:
# 	The first argument is the length of your text, in number of words
# 	The 'seedword' argument allows you to feed the bot some words that it
# 	should attempt to use to start its text. It's nothing fancy: the bot will
# 	simply try the first, and move on to the next if he can't find something
# 	that works.
my_first_text = tweetbot.generate_text(25, seedword=[u'ella', u'Alicia'])

# Print your text to the console
print(u'\ntweetbot says: "%s"' % (my_first_text))

 	
# # #
# TWITTER

# The MarkovBot uses @sixohsix' Python Twitter Tools, which is a Python wrapper
# for the Twitter API. Find it on GitHub: https://github.com/sixohsix/twitter

# Credentials

with open(text_filename, 'r') as f:
	twitter_credentials = json.load(f)

# Log in to Twitter
tweetbot.twitter_login(twitter_credentials['consumer_key'], 
                       twitter_credentials['consumer_secret'], 
                       twitter_credentials['access_key'], 
                       twitter_credentials['access_secret'])

# The target string is what the bot will reply to on Twitter. To learn more,
# read: https://dev.twitter.com/streaming/overview/request-parameters#track
targetstring = 'Orgullo Gay'
# Keywords are words the bot will look for in tweets it'll reply to, and it
# will attempt to use them as seeds for the reply
keywords = ['marriage', 'ring', 'flowers', 'children', 'religion']
# The prefix will be added to the start of all outgoing tweets.
prefix = None
# The suffix will be added to the end of all outgoing tweets.
suffix = '#OrgulloLGTBI'
# The maxconvdepth is the maximum depth of the conversation that the bot will
# still reply to. This is relevant if you want to reply to all tweets directed
# at a certain user. You don't want to keep replying in the same conversation,
# because that would be very annoying. Be responsible, and allow your bot only
# a shallow conversation depth. For example, a value of 2 will allow the bot
# to only reply in conversations where there are two or less replies to the
# original tweet.
maxconvdepth = None

# Start auto-responding to tweets by calling twitter_autoreply_start
# This function operates in a Thread in the background, so your code
# will not block by calling it.
tweetbot.twitter_autoreply_start(targetstring, keywords=None, prefix=None, suffix='Cada vez que se dice Orgullo Gay un Unicornio Marino muere... se dice Orgullo LGTBI ;-) #OrgulloLGTBI #OrgulloLGTBIQ', maxconvdepth=None)


# Start periodically tweeting. This will post a tweet every X days, hours, and
# minutes. (You're free to choose your own interval, but please don't use it to
# spam other people. Nobody likes spammers and trolls.)
# This function operates in a Thread in the background, so your code will not
# block by calling it.
tweetbot.twitter_tweeting_start(days=0, hours=2, minutes=0, keywords=None, prefix=None, suffix='#OrgulloLGTBI')

# DO SOMETHING HERE TO ALLOW YOUR BOT TO BE ACTIVE IN THE BACKGROUND
# You could, for example, wait for a week:
secsinweek = 7 * 24 * 60 * 60
time.sleep(secsinweek)
 
# Use the following to stop auto-responding
# (Don't do this directly after starting it, or your bot will do nothing!)
tweetbot.twitter_autoreply_stop()

# Use the following to stop periodically tweeting
# (Don't do this directly after starting it, or your bot will do nothing!)
tweetbot.twitter_tweeting_stop()
