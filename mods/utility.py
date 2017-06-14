from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import os
import tweepy

def set_password(password):
    return generate_password_hash(password)

def check_password(password):
    return check_password_hash(pw_hash, password)


consumer_token = os.environ['TW_CTOKEN']
consumer_secret = os.environ['TW_CSECRET']
access_token = os.environ['TW_ATOKEN']
access_token_secret = os.environ['TW_ASECRET']

def resolve_members(members):
	resolved_data = []

	for m in members:
		twit_username = m['twitter_username']
		insta_username = m['instagram_username']

		insta_url = "https://instagram.com/{}/?__a=1".format(insta_username)

		insta_user_data = json.loads(requests.get(insta_url).text)

		auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)

		twit_user_data = user = api.get_user(twit_username)
		temp_data = {
			"name":m['name'],
			"twitter_username":m['twitter_username'],
			"twitter_id": twit_user_data.id,
			"instagram_username":insta_username,
			"instagram_id":insta_user_data['user']['id'],
			"image_url":insta_user_data['user']['profile_pic_url']
		}

		resolved_data.append(temp_data)
	return resolved_data






if __name__ == "__main__":
	#test case
	mem = [
		{
			"name":"paras",
			"twitter_username":"paraazz",
			"instagram_username":"parazz_s"
		},

		{
			"name":"kanav",
			"twitter_username":"arorakanav11",
			"instagram_username":"arorakanav11"	
		}
	]

	print(resolve_members(mem))
