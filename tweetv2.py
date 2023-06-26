import tweepy
import os

from dotenv import load_dotenv
from ttmain import random_tweet
load_dotenv()



bearer_token = os.environ.get("BEARER_TOKEN")
print(bearer_token)

ttclient = tweepy.Client(bearer_token)

current_tweet = random_tweet()
print(current_tweet)
ttclient.create_tweet(text=current_tweet)
