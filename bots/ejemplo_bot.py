# -*- coding: utf-8 -*-

# Ejemplo de bot de Twitter - acciones básicas


import sys
import twitter

from akelarrebot import AkelarreBot

###
		
# Conectarse a la API
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

autenticacion = twitter.OAuth(access_key, access_secret, consumer_key, consumer_secret)
twitter_connection = twitter.Twitter(auth=autenticacion)
	

# Leer los tweets de una cuenta
tweets_medialab = twitter_connection.statuses.user_timeline(screen_name="medialabprado")
print('Tweets del timeline:\n')
print(tweets_medialab)


# Buscar tweets
tweets_akelarre = twitter_connection.search.tweets(q="#AkelarreCiberfeminista")
print('Tweets con el hashtag:\n')
print(tweets_akelarre)


# Publicar un tweet	
resp = twitter_connection.statuses.update(status="Esto es un tweet publicado desde la API REST :) #AkelarreCiberfeminista")
print('Tweet enviado. Respuesta:\n')
print(resp)


# Publicar un tweet	con imágenes

with open("imagen_ejemplo.jpg", "rb") as f:
    imagen = f.read()

twitterupload_connection = twitter.Twitter(domain='upload.twitter.com', auth=autenticacion)
imagen_id = twitterupload_connection.media.upload(media=imagen)["media_id_string"]
print('Imagen cargada. ID asignado:\n')
print(imagen_id)

resp = twitter_connection.statuses.update(status="Tweet con imagen desde la API REST: #AkelarreCiberfeminista", media_ids=imagen_id)
print('Tweet con imagen enviado. Respuesta:\n')
print(resp)



