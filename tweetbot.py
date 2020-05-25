import tweepy
import secrets
import time
import datetime
import os
import psycopg2
import random
import boto3

# -------------------------------------------------------------------

def random_tweet():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute("SELECT * FROM random_tweets ")
    rows = c.fetchall()
    random_tweet = rows[random.randint(0, len(rows) - 1)][1]
    c.close()
    return random_tweet



# -------------------------------------------------------------------
# This is the main script

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
api = tweepy.API(auth)

start_time = datetime.datetime.now()
api.update_status('TTBOT has started! ' + os.environ['TIM'] + ' ' + start_time.strftime("%c"))

print("Starting up! " + start_time.strftime("%c"))

# print(random_tweet())
api.update_status(random_tweet() + ' ' + start_time.strftime("%c"))


BUCKET_NAME = 'myttbucket'
OBJECT_NAME = 'images/lake-shore-road.jpg'
FILE_NAME = 'tmp/' + OBJECT_NAME.split("/")[-1]
print(FILE_NAME)
s4 = boto3.client('s3')
s4.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)

# print(random_tweet())
# api.update_status(random_tweet() + ' ' + start_time.strftime("%c"))
api.update_with_media(FILE_NAME, random_tweet() + ' ' + start_time.strftime("%c"))


while True:
    current_time = datetime.datetime.now()
    current_tweet = random_tweet() + ' ' + current_time.strftime("%c")
    api.update_status(current_tweet)
    print(current_tweet)
    time.sleep(3600)