import os
from dotenv import load_dotenv
import psycopg2

def test_connect():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT * FROM journal_entries WHERE id=213 """)
    query_results = cur.fetchall()
    print(query_results)

load_dotenv()

print(os.environ['TIM'])
print(os.environ['DATABASE_URL'])
test_connect()
