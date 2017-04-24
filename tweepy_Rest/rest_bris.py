import tweepy
import json
import couchdb
import jsonpickle
import sys,os
import time


maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
tweetCount = 0

oauth_keys = [["eNaOt7MW9SUk7zuPQpCrbXTBC", "agxEVyN5z6HtIv9LAK6CNmSU3dH194BMkuALb5oI9PU4Ui5dzK", "855999502255247360-Re3ewycQBkVi08w0rb1sp9bB40cLouA", "nisiRGg3tO50EMmbaU6MvAhnXYXe3FcQ0sjzkolDEPTyV"],
              ["ahAzM3Wvh4YITVM60G65ZuOpP", "NbWxlbuBsoDA4HELYWlyylY0RASjm0Gtbmsn9Vzbx10ZFXDAGv", "855999502255247360-BjSm0tFrw3v3um0QTRJ0wAvmhiy7cme", "kRUY3kM5MbBNryRDMA20EN7CNE7lSdJEg3FO3z7Omm1BH"],
              ["YFwd6NZlPBEm2Nu7VUs7eOXva", "ACa2A3C4RrV2TaSa9v1KF3ruO0zSZBC91RPYDh6K1XzYDY8rry", "855999502255247360-p93VgBZJIdb9254jAiCWzxCJ6RFJsLE", "Yrp1QszXQ2NUXJExQC4NR42ew4t7FpHKVD6EpJK8PBFZL"],
              ["ZQGDhawy20pPmyQmKQ79CtVNu", "Y1goSHJTe70CalKKBhT7EnGgkmiffnevmEvwG34z7IRjVVbBfb", "855999502255247360-wcivhMiEXhZHw5zyDJe0QhulwLaPFUW", "pvWGE9jNQyeHLnnMFkTbXniorXIjlDKuTDBxEPQRkLfXH"],
              ["ibSGx30BljiLofBRtS77AFETt", "4g2H14S8ugsPme1jELA6Y4O9RR5Sf8EElPLH96F5A8XFarl8VM", "855999502255247360-mwwO3oTq9TKhixLA8Exke4vgV1CnyfD", "med3gQXEWkKQtyC84zSDPIgCH3o2WrHGIx7fliTk6sJEf"]]

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
    db = couch['bris_tweets']
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
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry)
            else:
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry,
                                            since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry,
                                            max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q="place:004ec16c62325149", count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
        
        if not new_tweets:
            print "No more tweets found"
            time.sleep(180)
        
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

        print("Downloaded {0} tweets in Brisbane".format(tweetCount))   

    except tweepy.TweepError as e:
        print "switching keys...bris"
        switch += 1
        if switch > 4:
            print "Limit reached"
            switch = 0
            time.sleep(180)
         
        continue
    except StopIteration:
        break
