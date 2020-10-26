import os
import argparse
import psycopg2
import csv
from dotenv import load_dotenv
import boto3
import botocore
import s3fs
import os
import requests
import shutil

# --------------------------------------------------

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Media',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-m',
                        '--media',
                        help='Media',
                        metavar='media',
                        type=str,
                        default='tt1917.png')

    parser.add_argument('-r',
                        '--retrieve',
                        help='Retrieve Journal Entry ',
                        metavar='retrieve',
                        type=str,
                        default='1917 05 04')

    args = parser.parse_args()

    return args

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
    BUCKET_NAME = os.environ['S3_BUCKET']

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

            print('Image successfully Downloaded: ', filename)
            s4.upload_file(filename, BUCKET_NAME, filename)
            print('upload to amazon for next time!')
        else:
            print('Image Couldn\'t be retreived')
            # f_error.write(request_media)

        print('now let\'s try to get it to amazon s3')

        return filename


# --------------------------------------------------

def main():
    """Make a jazz noise here"""
    args = get_args()
    print("Media")
    print(args.media)
    filename = fetch_media(args.media)
    print(filename)

if __name__ == '__main__':
    load_dotenv()
    print(os.environ['S3_BUCKET'])
    main()
