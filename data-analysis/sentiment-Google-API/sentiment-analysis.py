import couchdb
from google.cloud import language

language_client = language.Client()
try:
    couch = couchdb.Server('http://localhost:15984/')
    print("Connect to local db")
except:
    print ("Cannot find CouchDB Server ... Exiting\n")
    print ("----_Stack Trace_-----\n")
    raise

db = couch['ten']
print ("Connecting to db: ten")
for each in db:
    try:
        text = db[each].get('text')
        document = language_client.document_from_text(text)
        sentiment = document.analyze_sentiment().sentiment
        score = sentiment.score
        print text +' ------------ '+ str(score)
    except Exception as e:
        print '******************'
        print Exception.message
        print text
        print '******************'
