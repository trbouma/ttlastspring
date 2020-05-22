import tweepy
import secrets
import time
import datetime

CONSUMER_KEY = 'iZA9WLoTfxmpGhYXETnAxrJKW'
CONSUMER_SECRET = 'Zjc6wxrJPG9ul67EMwon0ZkhImY2SaNCcpuIFoPk0kZJBWlKGJ'
ACCESS_KEY = '2855775129-w9bxpISeF4ORJ1muH327LHgecyeXeQQPBGxJsJX'
ACCESS_SECRET = 'uWrlbgafBxpW2GtoHtoTogIeJTiKakNT6JXbr1ukp1dZK'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# api.update_status(current_tweet)
# secrets.token_urlsafe(8)

while True:
    current_time = datetime.datetime.now()
    current_tweet = 'This is the time to really be! ' + current_time.strftime("%c")
    api.update_status(current_tweet)
    time.sleep(300)