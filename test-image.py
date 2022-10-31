from dotenv import load_dotenv
import tweepy
import os
import time, datetime


def get_filename(request_media):
    # Need to check if twitter URL filename= request_media.rstrip().split("/")[-1].split("?")[0]
    if "?" in request_media:
        retrieve_url = request_media.split("?")[0]
        # filename = file_prefix + request_media.rstrip().split("/")[-1].split("?")[0] + '.jpg'
    else:
        retrieve_url = request_media
        # filename = file_prefix + request_media.rstrip().split("/")[-1]

    filename = retrieve_url.rstrip().split("/")[-1]
    return filename


def twitter_update_with_media(current_tweet, with_media):
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])
    api = tweepy.API(auth)

    try:
        screen_name = api.verify_credentials().screen_name
        print("Authentication for media update OK:", screen_name)
    except:
        print("Error during authentication for media update")

    try:
        print("with_media:", with_media)
        api.update_status_with_media(filename=with_media,status=current_tweet)
        print("Status with media update OK")
        os.remove(with_media)
    except:
        print("Error during status and media update")

# ----------------------------------------

start_time = datetime.datetime.now()
load_dotenv()
print(get_filename("test.jpg"))
test_tweet = "Hello " + start_time.strftime("%c")
# test_image = "images/4YWjy.jpg"
test_image = "images/QDPqqnz.jpg"

twitter_update_with_media(test_tweet, test_image)
