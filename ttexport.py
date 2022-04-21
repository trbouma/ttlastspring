import os
import csv
from dotenv import load_dotenv
import psycopg2

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

load_dotenv()

print(os.environ['TIM'])
print(os.environ['DATABASE_URL'])
# test_connect()
# test_row_fetch()
# test_catalogue_export()
# test_tweet_export()
test_journal_export()
