from twython import Twython

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)

# search for tweets containing phrase 'data science'
for status in twitter.search(q='"data science"')["statuses"]:
    user = status["user"]["screen_name"].encode('utf-8')
    text = status["text"].encode('utf-8')
    print user, ":", text
    print

