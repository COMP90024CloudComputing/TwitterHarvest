import tweepy
import json
import couchdb
import jsonpickle
import sys,os
import time

maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
tweetCount = 0

oauth_keys = [["llx6OR7HIFWpAimFvxThRntdK", "WBuyh0IAEOMBPqKsyKnImjIvueej56NXNj5vHI3TlfweeDpgQi", "856001618545737728-BoqHNkQFVaNXClznkfDYhakgPWoud6z", "Cu4QIoz6mhUz9Qc4Ueugwy2whhXSfrs8aLD4pffrKQq64"],
              ["wXVze0342E0r9eeiIqgLsowrt", "jzLJKkcnfqyl0dwBVOFubR19rq3DCNuAWMmC79fkdXfAsatFfJ", "856001618545737728-Jxd8wRjkWGnMLN3he1D5OMQ1UuF7PhK", "vny6hRjaRmd2pTnB6DPMi7nfFHhz9mSPKzYiXzJrAhk0a"],
              ["54W4z7VC7Oob7aJR2TkrGTnzL", "1Ihs49YgblkMQEJzgvyqcnPTc9CBA2DmWlasvTGzSrzG7XUHkJ", "855999502255247360-RnabWffcqlxWw6ag1T5hd5Eymhg5rZn", "Pm1DT3EyHS8YVffnUZKs6lFKtfrN5eKVPDqLCA1Tv9dsd"],
              ["TcHoempgSuQkcbeIcBQPzLMqi", "VqNr0PugcJqHhwR8cHcI7ocRVDTcA5UAQGGpEoWHZJsIrY9Xuz", "839300214410207232-Jia98vmQtOIQaHhDDNCiJxtoJ9m35Hc", "qCGLAhGLqO58bkSOxymqP7v2fI6ISbBqlK2r39Emy2QhD"],              
              ["8hZKxdZp9ch6thyCI7tqx3WOg", "uqGOgnJMrpRToH2mwcMte2iFrTi9GmLBIQk3gTmoZkyF0495IJ", "856001618545737728-1REmFTyWkYvZJMjoqSD6yNi7Yr4Coqc", "poslWpf4yh9QSIMhGXyG6iSwQoP8LGFFH4MWs5UvvymcE"]]
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
    db = couch['mel_tweets']
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
                new_tweets = api.search(q="place:01864a8a64df9dc4", count=tweetsPerQry)
            else:
                new_tweets = api.search(q="place:01864a8a64df9dc4", count=tweetsPerQry,
                                            since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q="place:01864a8a64df9dc4", count=tweetsPerQry,
                                            max_id=str(max_id - 1))
            else:
                new_tweets = api.search(q="place:01864a8a64df9dc4", count=tweetsPerQry,
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

        print("Downloaded {0} tweets in Mel".format(tweetCount))   

    except tweepy.TweepError as e:
            
        print "switching keys...mel"
        switch += 1
        if switch > 4:
            print "Limit reached"
            switch = 0
            time.sleep(180)
         
        continue
    except StopIteration:
        break
