import pymongo
import os

db_url = os.environ['SBCON_DB']


def fetch_collection(collection):
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	coll = db[collection]
	data = []
	for i in coll.find():
		data.append(i)
	client.close()
	return data


def calculate_stats():
	client = pymongo.MongoClient(db_url)
	db = client.get_default_database()
	teams = fetch_collection("teams")

	STATS = []

	for t in teams:
		tw = []
		insta = []
		temp_stats = {
			"_id": t['_id'],
			"twitter" : {
				"twitter_likes": 0,
				"twitter_retweets": 0,
				"tweet_count":0
			},

			"instagram": {
				"instagram_post_count":0,
				"instagram_like":0,
				"instagram_comments":0,
			},
			"total_engagements":0,

		}

		#get username
		for m in t['members']:
			tw.append({"username": m['twitter_username']})
			insta.append({"owner_id": m['instagram_id']})

		# twitter stats
		coll = db['tweets_dump']
		TWC = coll.find({"$or": tw})
		n = TWC.count()
		temp_stats['twitter']['tweet_count'] = n
		for C in TWC:
			temp_stats['twitter']['twitter_likes']+=int(C['likes_count'])
			temp_stats['twitter']['twitter_retweets']+=int(C['retweets_count'])
		
		# instagram stats
		coll = db['insta_dump']
		IG = coll.find({"$or": insta})
		n = IG.count()
		temp_stats['instagram']['instagram_post_count']=n
		for C in IG:
			temp_stats['instagram']['instagram_like']+=int(C['like'])
			temp_stats['instagram']['instagram_comments']+=int(C['comments'])


		STATS.append(temp_stats)

	coll = db['stats']

	for d in STATS:
		coll.update_many({"_id":d['_id']}, {"$set": d}, upsert=True)

	client.close()


if __name__ == "__main__":
	print(calculate_stats())
