import tweepy
import os, psycopg2, random

from dotenv import load_dotenv
# from ttmain import random_tweet
from helpers import get_filename
import schedule, time

load_dotenv()

images_local = os.environ["IMAGES_LOCAL"]

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


bearer_token = os.environ.get("BEARER_TOKEN")
print(bearer_token)

# ttclient = tweepy.Client(bearer_token)

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

# media = api.media_upload(filename="/Users/trbouma/projects/ttlastspring/images/wMgLjzd.png")
# print("MEDIA: ", media)


# current_tweet = random_tweet()
# print(current_tweet)
# client.create_tweet(text=current_tweet, media_ids=[media.media_id_string])


if __name__ == "__main__":

    load_dotenv()

    schedule.every(1).to(4).hours.do(send_sketch)

    # send_sketch()
    print("Starting up!")

    while True:
        schedule.run_pending()
        time.sleep(1)