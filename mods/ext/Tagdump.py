import tweepy
import pprint
import os
import json
import requests
import pymongo
import datetime

consumer_token = os.environ['TW_CTOKEN']
consumer_secret = os.environ['TW_CSECRET']
access_token = os.environ['TW_ATOKEN']
access_token_secret = os.environ['TW_ASECRET']

db_url = os.environ['SBCON_DB']

def save_datas(data, collection):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db[collection]

	for d in data:
		coll.update_many({"post_id":d['post_id']}, {"$set": d}, upsert=True)
	print("Saved")
	client.close()

def update_last_id(l_id):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db["meta"]
	id  = coll.update_one({"id":"00"}, {"$set": {"last_id":l_id, "id":"00"}})
	print("Updated")
	client.close()



def hashtag_fetch_tw(hashtag, since_date):
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
			"post_id" : tweet.id,
			"tweet": tweet.text,
			"likes_count": tweet.favorite_count,
			"retweets_count": tweet.retweet_count,
			"username": tweet.user.screen_name.lower(),
			"created_at" : str(tweet.created_at),
			
		}
		data.append(temp_data)

	if len(data) >0:
		last_id = str(data[0]['post_id'])
		print(data)
		save_datas(data, "tweets_dump")
		update_last_id(last_id)

def hashtag_fetch_insta(hashtag):
	hashtag = hashtag.replace("#", "")
	get_posts = []
	explore_url = "https://www.instagram.com/explore/tags/{}/?__a=1".format(hashtag)

	d = json.loads(requests.get(explore_url).text)
	for p in d['tag']['top_posts']['nodes']: 
		temp_dict = {
				"post_id":p['id'],
				"owner_id":p['owner']['id'],
				"img_url":p['display_src'],
				"date":datetime.datetime.fromtimestamp(p['date']).strftime('%Y-%m-%d %H:%M:%S'),
				"caption":p['caption'],
				"like":p['likes']['count'],
				"comments":p['comments']['count']
			}
		get_posts.append(temp_dict)

	while 1:
		d = json.loads(requests.get(explore_url).text)
		for p in d['tag']['media']['nodes']:
			temp_dict = {
				"post_id":p['id'],
				"owner_id":p['owner']['id'],
				"img_url":p['display_src'],
				"date":datetime.datetime.fromtimestamp(p['date']).strftime('%Y-%m-%d %H:%M:%S'),
				"caption":p['caption'],
				"like":p['likes']['count'],
				"comments":p['comments']['count']
			}
			get_posts.append(temp_dict)
		if d['tag']['media']['page_info']['end_cursor'] == None:
			break
		explore_url = "https://www.instagram.com/explore/tags/{}/?__a=1&max_id={}".format(hashtag, 
																				d['tag']['media']['page_info']['end_cursor'])

	print(get_posts)
	save_datas(get_posts, "insta_dump")		
	




if __name__ == "__main__":
	hashtag_fetch_tw("lifeatstatusbrew", "2017-06-01")
	hashtag_fetch_insta("sbcon")
