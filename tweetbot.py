import tweepy
import secrets
import time
import datetime
import os
import psycopg2
import random
import boto3
import schedule

# -------------------------------------------------------------------

def random_tweet():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute("SELECT * FROM random_tweets ")
    rows = c.fetchall()
    random_tweet = rows[random.randint(0, len(rows) - 1)][1]
    c.close()
    return random_tweet

def random_status():

    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
    api = tweepy.API(auth)

    current_time = datetime.datetime.now()
    current_tweet = random_tweet() + ' ' + current_time.strftime("%c")
    api.update_status(current_tweet)
    print(current_tweet)

def real_time_tweet():
    # Get the current date and time
    currentDT = datetime.datetime.now()
    scheduled_month = str(currentDT.month).zfill(2)
    time_string = str(currentDT.day).zfill(2) + ' ' + str(currentDT.hour).zfill(2) \
                  + ' ' + str(currentDT.minute).zfill(2)
    print('real time: ' + scheduled_month + ' ' + time_string)
    scheduled_tweet = lookup_tweet(scheduled_month, time_string)
    if scheduled_tweet:
        if scheduled_tweet[3] == '' or scheduled_tweet[3] is None:
            print(scheduled_tweet[2] + 'No media!')
            twitter_update(scheduled_tweet[2])
        else:
            # local_media = fetch_media(scheduled_tweet[3])
            print(scheduled_tweet[2] , scheduled_tweet[3])
            twitter_update(scheduled_tweet[2])
            # twitter_update_with_media(scheduled_tweet[2], local_media)


def lookup_tweet(sched_month, time_string):
    # Lookup scheduled tweet
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute("SELECT * FROM tweets WHERE month=%s and daytime=%s", (sched_month, time_string))
    row = c.fetchone()
    c.close()
    return row

def twitter_update(current_tweet):

    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    try:
        api.update_status(current_tweet)
        print(current_tweet)
    except:
        print("Error during status update: " + current_tweet)

def twitter_update_with_media(current_tweet, with_media):


    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    try:
        api.update_with_media(with_media, status=current_tweet)
        print("Error during status and media update")
    except:
        print("Error during status and media update")


# -------------------------------------------------------------------
# This is the main script

start_time = datetime.datetime.now()
twitter_update('TTBOT has started! ' + os.environ['TIM'] + ' ' + start_time.strftime("%c"))

print("Starting up! " + start_time.strftime("%c"))

# print(random_tweet())
twitter_update(random_tweet() + ' ' + start_time.strftime("%c"))


BUCKET_NAME = 'myttbucket'
OBJECT_NAME = 'images/lake-shore-road.jpg'
FILE_NAME = 'tmp/' + OBJECT_NAME.split("/")[-1]
print(FILE_NAME)
s4 = boto3.client('s3')
s4.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)

# print(random_tweet())
# api.update_status(random_tweet() + ' ' + start_time.strftime("%c"))
twitter_update_with_media(random_tweet() + ' ' + start_time.strftime("%c"), FILE_NAME)

# Set up jobs that trigger at intervals
print("Set up scheduled jobs")
schedule.every(1).minutes.do(real_time_tweet)
schedule.every(30).minutes.do(random_status)


while True:
    schedule.run_pending()
    time.sleep(1)