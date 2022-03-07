cleaimport boto3
import botocore
import s3fs
import os
import requests
import shutil


def old_func():
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    BUCKET_NAME = 'ttbucket'
    OBJECT_NAME = '1tfLDVQ.jpg'
    FILE_NAME = '1tfLDVQ.jpg'

    s3_resource.Object(BUCKET_NAME, FILE_NAME).upload_file(Filename=FILE_NAME)


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

# ----------------------------------------------------------

BUCKET_NAME = 'myttbucket'
OBJECT_NAME = '1tfLDVQ.jpg'
FILE_NAME = '1tfLDVQ.jpg'


s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)

# data = open('import/images/1tfLDVQ.jpg','rb')
# s3.Bucket('myttbucket').put_object(Key='1tfLDVQ.jpg',Body=data)
    # s3.Bucket('myttbucket').

BUCKET_NAME = 'myttbucket'
OBJECT_NAME = 'images/lake-shore-road.jpg'
FILE_NAME = 'tmp/' + OBJECT_NAME.split("/")[-1]
print(FILE_NAME)
s4 = boto3.client('s3')
s4.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)


# Documentation is here: https://s3fs.readthedocs.io/en/latest/
s5 = s3fs.S3FileSystem()
print(OBJECT_NAME)
if s5.exists(BUCKET_NAME +"/"+ OBJECT_NAME):
    print('true!')

filename = fetch_media('http://www3.sympatico.ca/tim.bouma/anniversary/Image14.jpg')
# filename = fetch_media('https://i.imgur.com/b9chZhE.png')
print(filename)




# print(s4.upload_file(filename,BUCKET_NAME, filename ))
# os.remove(filename)
# s4.download_file(BUCKET_NAME, filename, filename)