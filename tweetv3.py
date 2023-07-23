import tweepy
import os, psycopg2, random, datetime

from dotenv import load_dotenv
# from ttmain import random_tweet
from helpers import get_filename
import schedule, time

load_dotenv()

images_local = os.environ["IMAGES_LOCAL"]

def twitter_update(scheduled_tweet: str, media_upload: str = None):

    # Authenticate to Twitter
    client = tweepy.Client(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token=os.environ.get("ACCESS_KEY"),
    access_token_secret=os.environ.get("ACCESS_SECRET")
    )


    auth = tweepy.OAuth1UserHandler(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token=os.environ.get("ACCESS_KEY"),
    access_token_secret=os.environ.get("ACCESS_SECRET")
    )

    api = tweepy.API(auth)
    if media_upload == None:
        client.create_tweet(text=scheduled_tweet)
    else:
        pass
        print("media upload", media_upload)
        media = api.media_upload(filename=media_upload)
        client.create_tweet(text=scheduled_tweet, media_ids=[media.media_id_string])

def send_sketch():

    images_local = os.environ["IMAGES_LOCAL"]

    client = tweepy.Client(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token=os.environ.get("ACCESS_KEY"),
    access_token_secret=os.environ.get("ACCESS_SECRET")
    )

    auth = tweepy.OAuth1UserHandler(
    consumer_key=os.environ.get("CONSUMER_KEY"),
    consumer_secret=os.environ.get("CONSUMER_SECRET"),
    access_token=os.environ.get("ACCESS_KEY"),
    access_token_secret=os.environ.get("ACCESS_SECRET")
    )
    
    api = tweepy.API(auth)

    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute("SELECT * FROM catalogue ")
    rows = c.fetchall()
    sketch_row = random.randint(0, len(rows) - 1)
    sketch_tweet = rows[sketch_row][2]
    sketch_media = rows[sketch_row][3]

    c.close()
    print("sketch media: ", sketch_media)
    local_media = get_filename(sketch_media)
    local_image = os.path.join(images_local,local_media)
    print("local image:", local_image)
    if os.path.isfile(local_image):
        print("image exists on file!")
        media = api.media_upload(filename=local_image)
        client.create_tweet(text=sketch_tweet, media_ids=[media.media_id_string])
        
    else:
        pass
        #twitter_update(sketch_tweet)

def lookup_tweet(sched_month, time_string):
    # Lookup scheduled tweet
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute("SELECT * FROM tweets WHERE month=%s and daytime=%s", (sched_month, time_string))
    row = c.fetchone()
    c.close()
    return row

def real_time_tweet():
   
    
    # Get the current date and time
    currentDT = datetime.datetime.now()
    scheduled_month = str(currentDT.month).zfill(2)
    time_string = str(currentDT.day).zfill(2) + ' ' + str(currentDT.hour).zfill(2) \
                  + ' ' + str(currentDT.minute).zfill(2)
    # print('real time: ' + scheduled_month + ' ' + time_string)
    scheduled_tweet = lookup_tweet(scheduled_month, time_string)
    # TODO write routine to determine if journal entry is being written
    # print(scheduled_tweet)
    if scheduled_tweet:
        if scheduled_tweet[4] == '' or scheduled_tweet[4] is None:
            print(scheduled_tweet[3] + 'with no media!')
            twitter_update(scheduled_tweet[3])
        else:
            # local_media = fetch_media(scheduled_tweet[3])
            print(scheduled_tweet[3] + "with media" + scheduled_tweet[4])
            # local_media = fetch_media(scheduled_tweet[4])
            local_media = get_filename(scheduled_tweet[4])
            
            local_image = os.path.join(images_local,local_media)

            twitter_update(scheduled_tweet[3], media_upload=local_image)




# bearer_token = os.environ.get("BEARER_TOKEN")
# print(bearer_token)

# ttclient = tweepy.Client(bearer_token)



# media = api.media_upload(filename="/Users/trbouma/projects/ttlastspring/images/wMgLjzd.png")
# print("MEDIA: ", media)


# current_tweet = random_tweet()
# print(current_tweet)
# client.create_tweet(text=current_tweet, media_ids=[media.media_id_string])


if __name__ == "__main__":

    load_dotenv()

    schedule.every(1).to(4).hours.do(send_sketch)
    schedule.every(1).minutes.do(real_time_tweet)

    send_sketch()
    print("Starting up!")

    while True:
        schedule.run_pending()
        time.sleep(1)