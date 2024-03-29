# https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43

# Import Data Journal Entries

# pushing local setup to heroku
# https://devcenter.heroku.com/articles/heroku-postgresql#local-setup

# A good DB utility app https://pgweb-demo.herokuapp.com/#

import os
import argparse
import psycopg2
import csv
from dotenv import load_dotenv


# TODO Clean up data files


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
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute("""SELECT count(*) FROM tweets""")
    query_results = cur.fetchall()
    print(query_results)


def journal_import(journal_file):
    # settings_data = settings.get_settings()

    conn = psycopg2.connect(os.environ['DATABASE_URL'])

    cur = conn.cursor()

    journal_dir = 'import/journal-entries/'
    # journal_file = '1917-05-04.txt'
    # create table journal_entries (journal_date text, journal_index text, journal_text text)

    file = open(journal_dir + journal_file)
    read_data = file.readlines()
    journal_date = journal_file.replace('.txt', '').replace('-', ' ')
    print(journal_date)
    # Delete existing rows
    cur.execute('DELETE FROM journal_entries WHERE journal_date LIKE %s', (journal_date,))
    conn.commit()

    warning = "WA"
    ok_length = "OK"
    max_length = 270
    tweet_out = []
    tweet_final = []
    row_index = 0
    for row in read_data:
        journal_text = row.strip()
        if (len(journal_text) > max_length):
            split_journal_text = journal_text.split(". ")
            for i in range(len(split_journal_text)):
                split_journal_text[i] = split_journal_text[i] + "."
            tweet_out.extend(split_journal_text)  # need to add back in period
        else:
            tweet_out.append(journal_text)

    # Combine shorter tweets into longer tweets

    # First line is the header line, so leave as is
    tweet_final.append(tweet_out[0])
    tweet_num = len(tweet_out)
    j = 1

    while j < tweet_num:
        if len(tweet_out[j]) > 250:
            print('A LONG SENTENCE!!')
            # Break into two
            mid_break = len(tweet_out[j])//2
            print(mid_break)
            tweet_final.append(tweet_out[j][0:mid_break])
            tweet_final.append(tweet_out[j][mid_break:len(tweet_out[j])])
            j +=1
        elif len(tweet_out[j]) > 140:
            tweet_final.append(tweet_out[j])
        else:
            # tweet is less than 140
            if j == tweet_num - 1:
                tweet_final.append(tweet_out[j])
            else:
                if len(tweet_out[j]) + len(tweet_out[j + 1]) < max_length:
                    tweet_final.append(tweet_out[j] + " " + tweet_out[j + 1])
                    j += 1
                else:
                    tweet_final.append(tweet_out[j])
        j += 1

    for row in tweet_final:
        row_index += 1
        journal_text = row.rstrip()
        length = len(journal_text)
        # print(journal_date, row_index,journal_text)
        print(f'({ok_length if length < max_length else warning}) {length}  {row_index} {journal_text}  ')
        cur.execute(""" INSERT INTO journal_entries (journal_date, journal_index, journal_text)
            VALUES (%s,%s,%s)""", (journal_date, row_index, journal_text))
    conn.commit()


def random_import():

    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    
    cur = conn.cursor()

    import_file = 'import/random/TTRandomTweets - tweets.csv'

    with open(import_file) as file:
        reader = csv.reader(file)
        for row in reader:
            print(row[0], row[1])
            cur.execute(""" INSERT INTO random_tweets (tweet)
             VALUES (%s)""", (row[1],))

    conn.commit()

def tweet_import():

    # cur = conn.cursor()

    # tweet_import_file = 'import/timeline/tweet-1917-03-24.csv'
    tweet_import_file = 'import/catalogue/catalogue.csv'

    with open(tweet_import_file) as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


    # conn.commit()


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

    print("Data Utilities")
    args = get_args()
    # test_connect()
    # catalogue_import()
    # random_import()
    # sched_tweet_import()
    # print(args)
    journal_import(args.journal)
    # tweet_import()
    # get_journal_entries(args.retrieve)
    # init_journal_entry(args.retrieve)
    # ttstatus.twitter_update(read_journal_entry())
    # print(read_journal_entry())


# --------------------------------------------------
if __name__ == '__main__':
    load_dotenv()
    main()
