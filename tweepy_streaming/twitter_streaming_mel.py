from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json
import jsonpickle
import sys,os

consumer_key="TcHoempgSuQkcbeIcBQPzLMqi"
consumer_secret="VqNr0PugcJqHhwR8cHcI7ocRVDTcA5UAQGGpEoWHZJsIrY9Xuz"
access_token="839300214410207232-Jia98vmQtOIQaHhDDNCiJxtoJ9m35Hc"
access_token_secret="qCGLAhGLqO58bkSOxymqP7v2fI6ISbBqlK2r39Emy2QhD"



try:
    couch = couchdb.Server('http://localhost:5984/')
    print("Connect to local db")
except:
    print ("Cannot find CouchDB Server ... Exiting\n")
    print ("----_Stack Trace_-----\n")
    raise

db = couch['mel_tweets']
print ("Connecting to db: mel")

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        try:
            tweet = json.loads(data)
        except Exception:
            print("Failed to parse tweet data")
            tweet = None

        db[tweet['id_str']]=tweet

        print("Saving text Mel")
        
        

    def on_status(self, status):
        print (status.next)
    def on_error(self, status):
        print (status)
    def on_timeout(self):
        print('Timeout...')
        return True   

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    l = StdOutListener()
    stream = Stream(auth, l)
    stream.filter(locations=[144,-38.03,146,-37]or 'Melbourne' in status.user.location.lower() ,async=True)
