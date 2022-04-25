import os
import csv
from dotenv import load_dotenv
import psycopg2
import boto3
import botocore
import s3fs

def file_exists_on_amazon(filename, bucketname):
    s5 = s3fs.S3FileSystem()
    s4 = boto3.client('s3')

    file_prefix = "images/"

    if s5.exists(bucketname + "/" + file_prefix + filename):
        print(f'{filename} exists on amazon!')
        return True
    else:
        print(f'{filename} DOES NOT EXIST on amazon!')
        return False

def test_connect():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT * FROM journal_entries WHERE id=213 """)
    query_results = cur.fetchall()
    print(query_results)

def test_row_fetch():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT * FROM journal_entries WHERE journal_date like '2020 01 05%' """)
    query_results = cur.fetchall()

    for one_row in query_results:
        print(one_row[3])

def test_catalogue_export():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT id, status, details, media, tags FROM catalogue """)
    query_results = cur.fetchall()

    with open('export/catalogue.csv','w') as csvfile:
        catalog_file = csv.writer(csvfile)
        for one_row in query_results:
            catalog_file.writerow(one_row)

def test_tweet_export():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT * FROM tweets """)
    query_results = cur.fetchall()

    with open('export/tweets.csv','w') as csvfile:
        catalog_file = csv.writer(csvfile)
        for one_row in query_results:
            catalog_file.writerow(one_row)

def test_journal_export():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT * FROM journal_entries """)
    query_results = cur.fetchall()

    with open('export/journal_entries.csv','w') as csvfile:
        catalog_file = csv.writer(csvfile)
        for one_row in query_results:
            catalog_file.writerow(one_row)

def process_catalogue_file():
    with open('export/catalogue.csv','r') as csvfile:
        catalog_file = csv.reader(csvfile)
        for id, status,description, request_media, tags in catalog_file:
            if "?" in request_media:
                request_media_out = request_media.split("?")[0].split("/")[-1]
            else:
                request_media_out = request_media.split("/")[-1]  
           
            print(id, request_media_out) 
            file_exists_on_amazon(request_media_out, 'myttbucket')
        




load_dotenv()

print(os.environ['TIM'])
print(os.environ['DATABASE_URL'])
# test_connect()
# test_row_fetch()
# test_catalogue_export()
# test_tweet_export()
# test_journal_export()
process_catalogue_file()
# file_exists_on_amazon('myttbucket','lake')
