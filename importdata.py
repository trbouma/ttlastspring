# https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43

# Import Data Journal Entries
# TODO Populate postgres with SQLITE3 data
# pushing local setup to heroku
# https://devcenter.heroku.com/articles/heroku-postgresql#local-setup

import os
import argparse
import psycopg2
import csv


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='TT Journal Import',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-j',
                        '--journal',
                        help='Journal Entry File',
                        metavar='journal',
                        type=str,
                        default='1917-05-04.txt')

    parser.add_argument('-r',
                        '--retrieve',
                        help='Retrieve Journal Entry ',
                        metavar='retrieve',
                        type=str,
                        default='1917 05 04')

    args = parser.parse_args()

    return args

# ----------------------------------------------------------------------------------------
def test_connect():

    # conn = psycopg2.connect(host="localhost", port=5432, database="ttdb", user="postgres", \
    #                        password="postgres")

    conn = psycopg2.connect('postgres://clelhjogzbfzmd:79c46b30cb390f16500d3f937f97722700f134daeaeea0da72a04b553cfffe60@ec2-54-81-37-115.compute-1.amazonaws.com:5432/dfn6u0pbnotebc?ssl=true')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM journal_entries""")
    query_results = cur.fetchall()
    print(query_results)


def journal_import(journal_file):
    # settings_data = settings.get_settings()

    # conn = sqlite3.connect('../data/scheduled-tweets.db')
    # conn = sqlite3.connect(settings_data["app_config"]["main_db"])
    # conn = psycopg2.connect(host="localhost", port=5432, database="ttdb", user="postgres", \
    #                        password="postgres")

    conn = psycopg2.connect('postgres://clelhjogzbfzmd:79c46b30cb390f16500d3f937f97722700f134daeaeea0da72a04b553cfffe60@ec2-54-81-37-115.compute-1.amazonaws.com:5432/dfn6u0pbnotebc?ssl=true')

    # DONE Use SQLITE for the database of tweets
    # DONE write import scripts for CSV file
    # TODO Write select statements for scheduler
    # TODO create table catalogue (status text, details text, media text, tags text)

    cur = conn.cursor()


    journal_dir = 'import/journal-entries/'
    # journal_file = '1917-05-04.txt'
    # create table journal_entries (journal_date text, journal_index text, journal_text text)

    file = open(journal_dir + journal_file)
    read_data = file.readlines()
    journal_date = journal_file.replace('.txt','').replace('-',' ')
    print(journal_date)
    # Delete existing rows
    cur.execute('DELETE FROM journal_entries WHERE journal_date LIKE %s',(journal_date,))
    conn.commit()

    warning = "WARNING!"
    ok_length = "OK"
    row_index = 0
    for row in read_data:
        row_index +=1
        journal_text = row.rstrip()
        length = len(journal_text)
        # print(journal_date, row_index,journal_text)
        print(f'{journal_date} {row_index} {journal_text} {length} ({ok_length if length < 200 else warning }) ')
        cur.execute(""" INSERT INTO journal_entries (journal_date, journal_index, journal_text)
            VALUES (%s,%s,%s)""", (journal_date,row_index,journal_text))
    conn.commit()

def random_import():

    conn = psycopg2.connect('postgres://clelhjogzbfzmd:79c46b30cb390f16500d3f937f97722700f134daeaeea0da72a04b553cfffe60@ec2-54-81-37-115.compute-1.amazonaws.com:5432/dfn6u0pbnotebc?ssl=true')
    cur = conn.cursor()

    import_file = 'import/random/TTRandomTweets - tweets.csv'

    with open(import_file) as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0], row[1])
            cur.execute(""" INSERT INTO random_tweets (tweet)
             VALUES (%s)""", (row[1],))

    conn.commit()
# --------------------------------------------------
def catalogue_import():
    # This imports data into the database

    conn = psycopg2.connect(os.environ['DATABASE_URL'])

    c = conn.cursor()

    # import_month = '12'
    import_file = 'import/TT Sketches - sketches2.csv'

    with open(import_file) as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0], row[1], row[2], row[3], row[4])
            c.execute(""" INSERT INTO catalogue (status, details, media, tags)
            VALUES (%s,%s,%s,%s)""", (row[0], row[1], row[2], row[3]))

    conn.commit()

def sched_tweet_import():
    # This imports data into the database

    conn = psycopg2.connect(os.environ['DATABASE_URL'])

    c = conn.cursor()

    import_file = 'import/December Tweets - tweets.csv'
    import_month = '12'

    with open(import_file) as file:
        reader = csv.reader(file)
        for row in reader:
            print(import_month, row[0], row[1], row[2])
            c.execute(""" INSERT INTO tweets (month, daytime, tweet, media)
            VALUES (%s,%s,%s,%s)""", (import_month, row[0], row[1], row[2]))

    conn.commit()

def main():
    """Make a jazz noise here"""

    print("Import Data")
    args = get_args()
    # test_connect()
    # catalogue_import()
    # random_import()
    sched_tweet_import()
    # print(args)
    # journal_import(args.journal)
    # get_journal_entries(args.retrieve)
    # init_journal_entry(args.retrieve)
    # ttstatus.twitter_update(read_journal_entry())
    # print(read_journal_entry())

# --------------------------------------------------


# --------------------------------------------------
if __name__ == '__main__':
    main()

