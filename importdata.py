# https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43

# TODO Populate postgres with SQLITE3 data

import psycopg2

conn = psycopg2.connect(host="localhost", port = 5432, database="ttdb", user="postgres", \
       password="postgres")
cur = conn.cursor()
cur.execute("""SELECT * FROM journal_entries""")
query_results = cur.fetchall()
print(query_results)