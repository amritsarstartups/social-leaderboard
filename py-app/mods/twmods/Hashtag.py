import tweepy
import pprint
import os

consumer_token = "8E17QEDQMdi8c2qdEG6bslpdg"
consumer_secret = "Hzrfjmy3e0KyuNEqrGOyUTXrDTKwmes0lWaAmOo7BlqKPHlUWZ"
access_token = "850697540-E6ccBsss0Lx3o1pxlXvRsaXPeWepWTUgvaybR0fq"
access_token_secret = "LgyrN8X0t5ynTcq8NwJ7Atehh0CrD7477wFUKf8NrEolM"


# consumer_token = os.environ['TW_CTOKEN']
# consumer_secret = os.environ['TW_CSECRET']
# access_token = os.environ['TW_ATOKEN']
# access_token_secret = os.environ['TW_ASECRET']

# db_url = os.environ['SBCON_DB']

def hashtag_fetch(hashtag, since_date):
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	HashTweet = tweepy.Cursor(api.search, q=hashtag, since=since_date).items()

	i = 0
	for tweet in HashTweet:
	    last_id=tweet.id
	    print(tweet.created_at, tweet.text, tweet.lang, tweet.id, tweet)
	    if i>1:
	    	break
	    i+=1

if __name__ == "__main__":
	hashtag_fetch("lifeatstatusbrew", "2017-06-01")