import tweepy
import json
import couchdb
import jsonpickle
import sys,os

maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
tweetCount = 0
max_id = -1

consumer_key = 'k687eBqLZnS6UOtx6etDg2UnX'
consumer_secret = 'aDbBWi9hAG703xNFXCTIEG6pB2qGsHLoUvvhIpnIjJZVbL4dBe'
access_token = '762662430-VfMM4zSLxQBtYNInjvwqaYbVKbOxfna5faf3u8J2'
access_secret = 'ZaJZzWt1zcwPd9yh4F64aLnfzg0PyJHUE0T8iXgU2yjce'

try:
    couch = couchdb.Server()
    print("Connect to remote db")
except:
    print "Cannot find CouchDB Server ... Exiting\n"
    print "----_Stack Trace_-----\n"
    raise

try:
    db = couch['syd']
    print "Using mydatabase bucket"
except:
    print ('error')
#Pass our consumer key and consumer secret to Tweepy's user authentication handler

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

#Pass our access token and access secret to Tweepy's user authentication handler
auth.set_access_token(access_token, access_secret)

#Creating a twitter API wrapper using tweepy
api = tweepy.API(auth)

#Error handling
if (not api):
    print ("Problem connecting to API")

api = tweepy.API(auth, #monitor_rate_limit=True, 
           retry_count=1000,retry_delay=5,retry_errors=set([401, 404, 500, 503]),
            	wait_on_rate_limit=True,
            		wait_on_rate_limit_notify=True)

places = api.geo_search(query="Sydney", granularity="city")
place_id = places[0].id

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L

while tweetCount < maxTweets:
    try:
        if max_id <= 0:
            if (not sinceId):
                new_tweets = api.search(q="place:%s" % place_id, count=tweetsPerQry)
            else:
                new_tweets = api.search(q="place:%s" % place_id, count=tweetsPerQry,
                                            since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q="place:%s" % place_id, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q="place:%s" % place_id, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
        
        if not new_tweets:
            print("No more tweets found")

        for tweet in new_tweets:
            data = json.loads(jsonpickle.encode(tweet._json))
            db.save(data)
            #print tweet.text +  '---' + tweet.place.name

        tweetCount += len(new_tweets)
        max_id = new_tweets[-1].id

    except tweepy.TweepError as e:
            # Just exit if any error
        print("some error : " + str(e))
        break
