from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import couchdb
import json
import jsonpickle
import sys,os

consumer_key="KuzAGiFtOlmYSbPVr1rBHgHL6"
consumer_secret="BHX5PJvjm1tx318ovvs65gAWeZoZARXwV9BZn2OAJwq4UPeo64"
access_token="839300214410207232-SJlWiB6lgyqF3kvyAoHdPvfa7dCPLpf"
access_token_secret="mX2lJ9lSViNvMw7ydSaLYZT9jT8YtfIxhW5j5cbQAF4Yj"

try:
    couch = couchdb.Server('http://localhost:5984/')
    print("Connect to local db")
except:
    print ("Cannot find CouchDB Server ... Exiting\n")
    print ("----_Stack Trace_-----\n")
    raise

db = couch['bris_tweets']
print ("Connecting to db: bris")

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

        try:
            db[tweet['id_str']]=tweet
            print("Saving text Bris")
        except:
            print('Skip duplicate tweet')

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
    stream.filter(locations=[152.7,-27.69,153.3,-27.06]or 'Brisbane' in status.user.location.lower(),async=True)
