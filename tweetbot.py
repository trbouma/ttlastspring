import tweepy
import secrets
import time
import datetime
import os
import psycopg2
import random
import boto3
import s3fs
import schedule
import requests
import shutil


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
    # print('real time: ' + scheduled_month + ' ' + time_string)
    scheduled_tweet = lookup_tweet(scheduled_month, time_string)
    # print(scheduled_tweet)
    if scheduled_tweet:
        if scheduled_tweet[4] == '' or scheduled_tweet[4] is None:
            print(scheduled_tweet[3] + 'No media!')
            twitter_update(scheduled_tweet[3])
        else:
            # local_media = fetch_media(scheduled_tweet[3])
            print(scheduled_tweet[3] + "with media" + scheduled_tweet[4])
            twitter_update(scheduled_tweet[3])
            local_media = fetch_media(scheduled_tweet[4])
            twitter_update_with_media(scheduled_tweet[3], local_media)


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
        print("Authentication for media update OK")
    except:
        print("Error during authentication for media update")

    try:
        api.update_with_media(with_media, status=current_tweet)
        print("Status with media update OK")
        os.remove(with_media)
    except:
        print("Error during status and media update")


def fetch_media(request_media):
    # TODO Fetch media - input a request determine if filename or url
    s5 = s3fs.S3FileSystem()
    s4 = boto3.client('s3')

    file_prefix = "images/"

    # Need to check if twitter URL filename= request_media.rstrip().split("/")[-1].split("?")[0]
    if "?" in request_media:
        retrieve_url = request_media.split("?")[0] + '.jpg'
        # filename = file_prefix + request_media.rstrip().split("/")[-1].split("?")[0] + '.jpg'
    else:
        retrieve_url = request_media
        # filename = file_prefix + request_media.rstrip().split("/")[-1]

    filename = file_prefix + retrieve_url.rstrip().split("/")[-1]

    print(retrieve_url)
    print(filename)

    # First check to see if already on amazon
    BUCKET_NAME = 'myttbucket'

    if s5.exists(BUCKET_NAME + "/" + filename):
        print('exists on amazon!')
        s4.download_file(BUCKET_NAME, filename, filename)
        return filename

    if os.path.isfile(filename):
        print(filename + " It is a file!")

        return filename
    else:
        print(filename + " It is not a file! Let's try to get it")
        r = requests.get(retrieve_url, stream=True)
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', filename)
            s4.upload_file(filename, BUCKET_NAME, filename)
            print('upload to amazon for next time!')
        else:
            print('Image Couldn\'t be retreived')
            # f_error.write(request_media)

        print('now let\'s try to get it to amazon s3')

        return filename

# -------------------------------------------------------------------
# This is the main script

start_time = datetime.datetime.now()
twitter_update('TTBOT has started! ' + os.environ['TIM'] + ' ' + start_time.strftime("%c"))

print("Starting up! " + start_time.strftime("%c"))

# print(random_tweet())
twitter_update(random_tweet() + ' ' + start_time.strftime("%c"))


# print(random_tweet())
# api.update_status(random_tweet() + ' ' + start_time.strftime("%c"))
FILE_NAME = fetch_media('http://www3.sympatico.ca/tim.bouma/images/backroad9.jpg')
twitter_update_with_media(random_tweet() + ' ' + start_time.strftime("%c"), FILE_NAME)


# Set up jobs that trigger at intervals
print("Set up scheduled jobs")
schedule.every(1).minutes.do(real_time_tweet)
schedule.every(30).minutes.do(random_status)

while True:
    schedule.run_pending()
    time.sleep(1)