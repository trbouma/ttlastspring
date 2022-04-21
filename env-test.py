import os
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

def test_catalogue_fetch():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT count(*) FROM catalogue """)
    query_results = cur.fetchall()

    for one_row in query_results:
        print(one_row)

load_dotenv()

print(os.environ['TIM'])
print(os.environ['DATABASE_URL'])
# test_connect()
# test_row_fetch()
test_catalogue_fetch()
