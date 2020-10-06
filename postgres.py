# https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43

# TODO Populate postgres with SQLITE3 data

import psycopg2

# conn = psycopg2.connect(host="localhost", port = 5432, database="ttdb", user="postgres", \
#       password="postgres")

# conn = psycopg2.connect('postgres://clelhjogzbfzmd:79c46b30cb390f16500d3f937f97722700f134daeaeea0da72a04b553cfffe60@ec2-54-81-37-115.compute-1.amazonaws.com:5432/dfn6u0pbnotebc?ssl=true')
conn = psycopg2.connect('postgres://oqiwumuzjwisbo:f111a3a4ad2eda7a9881197fe30a5a779e64cb333228c5e22eec17e9d3a26f25@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d7lsopmj5cdvou')

cur = conn.cursor()
cur.execute("""SELECT count(*) FROM tweets""")
query_results = cur.fetchall()
print(query_results)