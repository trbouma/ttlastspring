import tweepy
import secrets
import time
import datetime
import os

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
api = tweepy.API(auth)

start_time = datetime.datetime.now()
api.update_status('TTBOT has started! ' + os.environ['TIM'] + ' ' + start_time.strftime("%c"))

print("Starting up! " + start_time.strftime("%c"))

while True:
    current_time = datetime.datetime.now()
    current_tweet = 'This is the time to really be! ' + current_time.strftime("%c")
    api.update_status(current_tweet)
    print(current_tweet + ' ' + current_time.strftime("%c"))
    time.sleep(3600)