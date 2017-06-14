import tweepy
import pprint
import os
import json
import pymongo


consumer_token = os.environ['TW_CTOKEN']
consumer_secret = os.environ['TW_CSECRET']
access_token = os.environ['TW_ATOKEN']
access_token_secret = os.environ['TW_ASECRET']

db_url = os.environ['SBCON_DB']

def save_datas(data, collection):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db[collection]
	id  = coll.insert_many(data)
	print("Saved")
	client.close()

def update_last_id(l_id):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db["meta"]
	id  = coll.update_one({"id":"00"}, {"$set": {"last_id":l_id, "id":"00"}})
	print("Updated")
	client.close()



def hashtag_fetch(hashtag, since_date):
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db["meta"]
	last_id  = coll.find_one()['last_id']
	client.close()
	print(last_id)
	HashTweet = tweepy.Cursor(api.search, q=hashtag, since=since_date, since_id=int(last_id)).items()
	data = []
	for tweet in HashTweet:
		temp_data = {
			"tweet": tweet.text,
			"likes_count": tweet.favorite_count,
			"retweets_count": tweet.retweet_count,
			"username": tweet.user.screen_name,
			"created_at" : str(tweet.created_at),
			"tweet_id" : tweet.id
		}
		data.append(temp_data)

	if len(data) >0:
		last_id = str(data[0]['tweet_id'])
		print(data)
		save_datas(data, "tweets_dump")
		update_last_id(last_id)
	    

if __name__ == "__main__":
	hashtag_fetch("lifeatstatusbrew", "2017-06-01")
