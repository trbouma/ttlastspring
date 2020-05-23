# https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43

import psycopg2

conn = psycopg2.connect(host="localhost", port = 5432, database="postgres", user="postgres", \
       password="postgres")
cur = conn.cursor()
cur.execute("""SELECT * FROM playground""")
query_results = cur.fetchall()
print(query_results)