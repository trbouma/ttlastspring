import tweepy
import secrets
import time

CONSUMER_KEY = 'iZA9WLoTfxmpGhYXETnAxrJKW'
CONSUMER_SECRET = 'Zjc6wxrJPG9ul67EMwon0ZkhImY2SaNCcpuIFoPk0kZJBWlKGJ'
ACCESS_KEY = '2855775129-w9bxpISeF4ORJ1muH327LHgecyeXeQQPBGxJsJX'
ACCESS_SECRET = 'uWrlbgafBxpW2GtoHtoTogIeJTiKakNT6JXbr1ukp1dZK'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# api.update_status(current_tweet)


while True:
    current_tweet = 'This is the time to really ex be! ' + secrets.token_urlsafe(8)
    api.update_status(current_tweet)
    time.sleep(1800)