import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import couchdb

consumer_key = 'k687eBqLZnS6UOtx6etDg2UnX'
consumer_secret = 'aDbBWi9hAG703xNFXCTIEG6pB2qGsHLoUvvhIpnIjJZVbL4dBe'
access_token = '762662430-VfMM4zSLxQBtYNInjvwqaYbVKbOxfna5faf3u8J2'
access_secret = 'ZaJZzWt1zcwPd9yh4F64aLnfzg0PyJHUE0T8iXgU2yjce'

'''
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text) 
'''
try:
    couch = couchdb.Server()
    print("Connect to db")
except:
    print "Cannot find CouchDB Server ... Exiting\n"
    print "----_Stack Trace_-----\n"
    raise


db = couch['syd']
print "Using mydatabase bucket"


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
    def on_status(self, status):
        print 'Ran on_status'

    def on_data(self, data):
        try:
            tweet = json.loads(data)
        except Exception:
            print("Failed to parse tweet data")
            tweet = None

        db.save(tweet)
        	
        #if 'melbourne' in status.user.location.lower():
        print('Saving text')
        # There are many options in the status objtect,
        # hashtags can be very easily accessed.
        #for hashtag in status.entries['hashtags']:
        #    print(hashtag['text'])
 
 
    def on_error(self, status):
    	if status_code == 420:
            return False
        print('Got an error:' + status)
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    stream = Stream(auth, listener)
    stream.filter(locations=[150.52,-34.09,151.25,-33.48] or 'sydney' in status.user.location.lower())