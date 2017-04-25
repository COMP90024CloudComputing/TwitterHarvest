from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json
import jsonpickle
import sys,os

consumer_key="hVExlxALeBFp9CSLP5KfRMyhr"
consumer_secret="sRmuFRKdYUDJgteteXvDDE5LlpzgtGXY9bwuisZV4usv92zEVh"
access_token="851278815812755456-WwP50uxcaWt3NTDfFCXuIEmFz72iOfy"
access_token_secret="TTnhP9lIlfO1EhvAzRS8BlLl9FY7OCgk7pvRISJonWF2y"

try:
    couch = couchdb.Server('http://localhost:5984/')
    print("Connect to local db")
except:
    print ("Cannot find CouchDB Server ... Exiting\n")
    print ("----_Stack Trace_-----\n")
    raise

db = couch['ade_tweets']
print ("Connecting to db: ade")

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_status(self, status):
        print ('Run on status')
        

    def on_data(self, data):
        try:
            tweet = json.loads(data)
        except Exception:
            print("Failed to parse tweet data")
            tweet = None

        try:
            db[tweet['id_str']]=tweet
            print("Saving text Ade")
        except:
            print('Skip duplicate tweet')
            
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
    stream.filter(locations=[138.4,-35.27,138.76,-34.58] or 'Adelaide' in status.user.location.lower() ,async=True)
