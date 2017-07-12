# -*- coding: utf-8 -*-

# AkelarreBot - Mejora sobre MarkovBot para incorporar funcionalidades de defensa ciberfeminista
# Version 0.1

import sys
import os
import time
import json

from threading import Thread, Lock

from markovbot import MarkovBot, IMPTWITTER
	
###

class AkelarreBot(MarkovBot):
	
	def __init__(self, recop_filepath, chainlength=3):
		super(AkelarreBot, self).__init__(chainlength)
		
		# Comprobar que se puede escribir en el fichero
		self.recop_filepath = recop_filepath
		try:
			with open(self.recop_filepath, 'a') as f:
				f.write('')
		except Exception as e:
			print("Error al intentar escribir en el fichero de recopilación")
			raise e
		
		self.troll_data = {}
				
		# Preparar el hilo de autorecopilación de trolls
		self._autorecopilacion = False
		self._autorecopilacion_keywords = None
		if IMPTWITTER:
			self._autorecopilacionthreadlives = True
			self._autorecopilacionthread = Thread(target=self._autorecopilaciontrolls)
			self._autorecopilacionthread.daemon = True
			self._autorecopilacionthread.name = u'autorecopilador'
		else:
			self._autorecopilacionthreadlives = False
		
		
		if IMPTWITTER:
			self._autorecopilacionthread.start()
	
		
	def twitter_autorecopilaciontrolls_start(self, hechizos_invocacion):
		
		"""Inicia el hilo interno que escucha el hechizo de invocación
		e incorpora a la lista de trolls la cuenta del tweet al que se esté contestando.
		
		Argumentos
		
		hechizo_invocacion	-	Lista de palabra(s) que se van a utilizar para marcar un troll
		                        y de las que hay que realizar seguimiento.
		
		"""
		
		# Raise an Exception if the twitter library wasn't imported
		if not IMPTWITTER:
			self._error(u'twitter_autorecopilaciontrolls_start', \
				u"The 'twitter' library could not be imported. Check whether it is installed correctly.")
		
		# Hasta que no se conecte a Twitter no podrá empezar a leer
		if not self._loggedin:
			self._message(u'twitter_autorecopilaciontrolls_start', \
				u"Not logged in to Twitter yet. I'll wait until you call the twitter_login() function...")
				
		# hechizos_invocacion tiene que ser un string con las keywords separadas por ","
		# (formato para el método track de la Api Streaming de Twitter)
		if type(hechizos_invocacion) in [str, unicode]:
			hechizos_invocacion = hechizos_invocacion.replace(',', '')
		else:
			hechizos_invocacion = ','.join([h.replace(',', '') for h in hechizos_invocacion])
		
		# Actualizar parámetros 
		self._autorecopilacion_keywords = hechizos_invocacion
		
		# Señal para que el hilo de autorecopilación empiece
		self._autorecopilacion = True
		
		self._message(u'twitter_autorecopilaciontrolls_start', u"I'm ready! Waiting for invocations...")
	
	
	def twitter_autorecopilaciontrolls_stop(self):
		
		"""Desactiva el hilo de recopilación de trolls.
		"""
		
		# Actualizar parámetros
		self._autorecopilacion_keywords = None
		
		# Señal para que el hilo de autorecopilación pare
		self._autorecopilacion = False
	

	def _autorecopilaciontrolls(self):
		
		"""Monitoriza Twitter Strem y anota la cuenta de los tweets 
		   a los que se haya contestado con algún hechizo de invocación.
		"""
		
		# Run indefinitively
		while self._autorecopilacionthreadlives:

			# Wait a bit before rechecking whether autorecopilacion should be
			# started. It's highly unlikely the bot will miss something if
			# it is a second late, and checking continuously is a waste of
			# resource.
			time.sleep(1)
			
			# Only start when the bot logs in to twitter, and when a
			# target string is available
			if self._loggedin and self._autorecopilacion_keywords is not None:
			
				while self._autorecopilacion: # Puede activarse y desactivarse
				
					# Check whether the other Threads are still alive, 
					# and revive if they aren't.
					self._cpr() #TODO
					
					# Pedir tweets nuevos que contengan las keywords
					self._tslock.acquire(True)
					tweet_iterator = self._ts.statuses.filter(track=self._autorecopilacion_keywords)
					self._tslock.release()
						
					# Get a new Tweet (this will block until a new tweet becomes available, 
					# but can also raise a StopIteration Exception every now and again)
					try:
						tweet = next(tweet_iterator)
					except StopIteration:
						# Restart the iterator, and skip the rest of the loop.
						self._tslock.acquire(True)
						tweet_iterator = self._ts.statuses.filter(track=self._autorecopilacion_keywords)
						self._tslock.release()
						continue
						
					# Restart the connection if this is a 'hangup'
					# notification, which will be {'hangup':True}
					if u'hangup' in tweet.keys():
						# Reanimate the Twitter connection.
						self._twitter_reconnect()
						continue
					
					#TODO Control anti-trolleo contra el propio bot
						
					# Only proceed if autorecopilacion is still required (there
					# can be a delay before the iterator produces a new, and
					# by that time autoreplying might already be stopped)
					if not self._autorecopilacion:
						continue

					# Report to console
					self._message(u'_autorecopilaciontrolls', u"I've found a new tweet!")
					
					# Si el tweet no es una respuesta de otro, ignorar
					tweet_original = tweet[u'in_reply_to_status_id_str']
					if tweet_original is None:
						# Skip one cycle, which will bring us to the next tweet
						self._message(u'_autorecopilaciontrolls', \
							u"This tweet was not a reply. Skipping...")
						continue
										
					self._tlock.acquire(True)
					tweet_original = self._t.statuses.show(id=tweet_original)
					self._tlock.release()
					
					troll = tweet_original[u'user']
					
					if troll[u'id_str'] in self.troll_data.keys():
						self._message(u'_autorecopilaciontrolls', \
							u"Found troll! Already in the database, updating information.")
						self.troll_data[troll[u'id_str']].add(troll[u'screen_name'])
					else:
						self._message(u'_autorecopilaciontrolls', \
							u"Found new troll! Handle: " + troll[u'screen_name'] + ". Adding it to the database and updating file.")
						self.troll_data[troll[u'id_str']] = set(troll[u'screen_name'])
						with open(self.recop_filepath, 'a') as f:
							f.write(troll[u'id_str'] + "\n")		
