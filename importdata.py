# https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43

# Import Data Journal Entries
# TODO Populate postgres with SQLITE3 data
# pushing local setup to heroku
# https://devcenter.heroku.com/articles/heroku-postgresql#local-setup


import argparse

import psycopg2


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

    conn = psycopg2.connect(host="localhost", port=5432, database="ttdb", user="postgres", \
                            password="postgres")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM journal_entries""")
    query_results = cur.fetchall()
    print(query_results)


def journal_import(journal_file):
    # settings_data = settings.get_settings()

    # conn = sqlite3.connect('../data/scheduled-tweets.db')
    # conn = sqlite3.connect(settings_data["app_config"]["main_db"])
    conn = psycopg2.connect(host="localhost", port=5432, database="ttdb", user="postgres", \
                            password="postgres")

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


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    print("Import Data")
    args = get_args()
    test_connect()
    print(args)
    journal_import(args.journal)
    # get_journal_entries(args.retrieve)
    # init_journal_entry(args.retrieve)
    # ttstatus.twitter_update(read_journal_entry())
    # print(read_journal_entry())

# --------------------------------------------------


# --------------------------------------------------
if __name__ == '__main__':
    main()

