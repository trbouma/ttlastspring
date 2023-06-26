import tweepy 
import os
from dotenv import load_dotenv
from ttmain import random_tweet
load_dotenv()  


auth = tweepy.OAuth1UserHandler(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token=os.environ.get("ACCESS_KEY"),
    access_token_secret=os.environ.get("ACCESS_SECRET")
    )

api = tweepy.API(auth)

media = api.media_upload(filename="/Users/trbouma/projects/ttlastspring/images/wMgLjzd.png")
print("MEDIA: ", media)

current_tweet = random_tweet()

# tweet = api.update_status(status=current_tweet, media_ids= 
#    [media.media_id_string])
# print("TWEET: ", tweet)