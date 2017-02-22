import sys

import json
import socket

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

class TweetsListener(StreamListener):

	def __init__(self,socket):
		print ("Tweet listener initialized")
		self.client_socket = socket

	def on_data(self, data):
		try:
			jsonMessage = json.loads(data)
			message = jsonMessage['text'].encode('utf-8')
			print (message)
			self.client_socket.send(message)
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		print (status)
		return True
	
def connect_to_twitter(connection):
	api_key = "0D5JvZZ6DezvAdxR54aPlI9FI"
	api_secret = "gTpG7zuBYVddpU1hslEvSZbtHC5ucAzP2OSeKd6HqJE9cdXfZS"

	access_token = "834329287813689344-9C64qjnjKJk9DpXSHkKZp85EGxOboFJ"
	access_token_secret = "HofcloqZAyzxrcwyJSJFGKbO9UEPIxMAqU5TL9P8htLpe"

	auth = OAuthHandler(api_key, api_secret)
	auth.set_access_token(access_token, access_token_secret)

	twitter_stream = Stream(auth, TweetsListener(connection))
	twitter_stream.filter(track=['#'])


if __name__ == "__main__":
	soc = socket.socket()
	host="localhost"
	port=7789
	soc.bind((host,port))

	print("Listening on port : %s" % str(port))

	soc.listen(5)

	connection, address = soc.accept()

	print ("Received request from: " + str(address))
	
	connect_to_twitter(connection)













