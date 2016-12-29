from twython import TwythonStreamer
from collections import Counter

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

tweets = []

class MyStreamer(TwythonStreamer):

    def on_success(self, data):

        if data['lang'] == 'en':
            tweets.append(data)
            print "received tweet #", len(tweets)

            if len(tweets) >= 100:
                self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET,
                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

stream.statuses.filter(track='data')

top_hashtags = Counter(hashtag['text'].lower()
                       for tweet in tweets
                       for hashtag in tweet['entities']["hashtags"])

print top_hashtags.most_common(5)
