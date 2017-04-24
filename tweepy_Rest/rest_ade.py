import tweepy
import json
import couchdb
import jsonpickle
import sys,os
import time


maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
tweetCount = 0

oauth_keys = [["RjG2NW31P2LBR14iBcl2NTtHQ", "j7Z81CvuoxlmnirBaXYvv0ncugs2qqkBhosxomwOEYESJlokO8", "856109659895218178-JwIbrtpRreIXULwSDsgS6Y9vqUjUZSz", "6gc4AOswm7ZqAebJ4VE8KItobluFcM7KZrjNPVltuTt6j"],
              ["0OfIH1dCTHAuf5B3K8gy9Ni4X", "9BfIHjGoKLQMISkSFdc7L014RYjvQv74JowHeBbiLQ0yhksYVk", "856109659895218178-2ahh1Em96SjiGVKps00GZHy32US0ZVF", "srM8nm9z0y6sYHeeV2fv6Dxom2V60GfrqkmNHOCnn36LV"],
              ["p6atboVqe2eN5VrXHGeh0YOuF", "UmpTijm7MpXEs9AXTDRznWhPfrhkbtkIDfQiBwnJN9dlBwBJNz", "839300214410207232-p5KRSFi3c7WLlbma9sP3cRpfX1nAoQn", "JZdKxShEDrTfNj7JMMWIR31exHNSoqzLmNzLzscZj03JF"],
              ["hVC7zPDwRBni2lIfZDQiKdVTb", "fvWPF5tEkMEyZp9e0yQOIi9a3kzl3Bjfa1b1SfYFxjomgxHNQr", "856002238250012672-WOGROUddQLJI92zQYl07xK9zktEHN6a", "ll9lhJwZDuKIuEsviiKdeXPlpuZbyXTAN1ss6QZxiasXl"],              
              ["GuqJrIAlenTWGJoQDXuLI78G6", "X8QGSq5cogeOBMAjrlZOO1Kh1puoIhKXuHhz80PVcq6BxOIkgb", "856109659895218178-1ON36X1qYHe7FgWY9AJOCMQ6yXV8KTq", "DUjbcjp2t5SHTXVnHQj0KLwN9WEYacD1sZCYqHLz8gNDC"]]
'''
consumer_key = 'k687eBqLZnS6UOtx6etDg2UnX'
consumer_secret = 'aDbBWi9hAG703xNFXCTIEG6pB2qGsHLoUvvhIpnIjJZVbL4dBe'
access_token = '762662430-VfMM4zSLxQBtYNInjvwqaYbVKbOxfna5faf3u8J2'
access_secret = 'ZaJZzWt1zcwPd9yh4F64aLnfzg0PyJHUE0T8iXgU2yjce'
'''
try:
    couch = couchdb.Server()
    print("Connect to remote db")
except:
    print "Cannot find CouchDB Server ... Exiting\n"
    print "----_Stack Trace_-----\n"
    raise

try:
    db = couch['ade_tweets']
    print "Using mydatabase bucket"
except:
    print ('error')


auths = []  
for consumer_key, consumer_secret, access_key, access_secret in oauth_keys:  
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
    auth.set_access_token(access_key, access_secret)  
    auths.append(auth)

#Pass our consumer key and consumer secret to Tweepy's user authentication handler

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

#Pass our access token and access secret to Tweepy's user authentication handler
#auth.set_access_token(access_token, access_secret)

#Creating a twitter API wrapper using tweepy

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L
switch = 0
while tweetCount < maxTweets:
    

    api = tweepy.API(auths[switch], #monitor_rate_limit=True, 

        #retry_count=10000, retry_delay=5, 
         #   retry_errors=set([401, 404, 500, 503]),
                #wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
    
    #Error handling
    if (not api):
        print ("Problem connecting to API")

    try:
        if max_id <= 0:
            if (not sinceId):
                new_tweets = api.search(q="place:01e8a1a140ccdc5c", count=tweetsPerQry)
            else:
                new_tweets = api.search(q="place:01e8a1a140ccdc5c", count=tweetsPerQry,
                                            since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q="place:01e8a1a140ccdc5c", count=tweetsPerQry,
                                            max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q="place:01e8a1a140ccdc5c", count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
        
        if not new_tweets:
            print "No more tweets found"
            time.sleep(240)

            '''
            print "switching keys..."
            switch += 1
            if switch > 2:
                print "Limit reached"
                switch = 0
            continue  
            '''

        for tweet in new_tweets:
            data = json.loads(jsonpickle.encode(tweet._json))
            try:
                db[data['id_str']]=data
            except:
                print 'Skip update error'
            #print tweet.place.name# +  '---' + tweet.place.name

        tweetCount += len(new_tweets)
        
        try:
            max_id = new_tweets[-1].id
        except :
            continue

        print("Downloaded {0} tweets in Adelaide".format(tweetCount))   

    except tweepy.TweepError as e:
        
        print "switching keys...ade"
        switch += 1
        if switch > 4:
            print "Limit reached"
            switch = 0
            time.sleep(180)

        continue
    except StopIteration:
        break
