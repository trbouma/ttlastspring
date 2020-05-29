import psycopg2
import os
import datetime
import argparse


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


def init_journal_entry(journal_date):
    # Sets up journal entry for requested date

    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute('select count(*) from journal_entries where journal_date = %s ', [journal_date])
    row = c.fetchone()
    # print(row[0])

    journal_max = row[0]
    journal_index = 1
    journal_state = 'WRITE' if journal_max > 0 else 'DONE'

    c = conn.cursor()
    c.execute('delete from journal_status')
    c.execute(""" INSERT INTO journal_status (journal_date, journal_max, journal_index,journal_state)
    VALUES (%s,%s,%s,%s)""", (journal_date, journal_max, journal_index, journal_state))
    conn.commit()
    conn.close()


def read_journal_entry():
    # This the reading
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    c = conn.cursor()
    c.execute('select * from journal_status')
    row = c.fetchone()
    journal_date, journal_max, journal_index, write_status = row[1], row[2], row[3], row[4]
    # print(journal_date, journal_max, journal_index,write_status)
    # get journal entry then increment
    # need to check write status
    if write_status.upper() == 'WRITE':
        c.execute('''select * from journal_entries 
        where journal_date = %s and journal_index = %s''', (journal_date, journal_index))
        row_journal = c.fetchone()

        journal_update = row_journal[3]
        journal_index += 1
        # TODO The last line is DONE - it should be WRITE
        write_status = 'WRITE' if journal_index <= journal_max else 'DONE'
        # TODO Add final end checking
        c.execute('''update journal_status set journal_index = %s, journal_state = %s 
        where journal_date = %s ''', (journal_index, write_status, journal_date,))
        conn.commit()
        conn.close()
        return journal_update
    else:
        return "DONE"


def ready_to_write_journal():
    # TODO This will be the daily to set up to do the series of tweets from the journal entry.

    currentDT = datetime.datetime.now()
    journal_year = "1917 " if currentDT.month < 9 else "1916 "
    journal_date = journal_year + str(currentDT.month).zfill(2) + " " + str(currentDT.day).zfill(2)

    print("Getting ready to write my journal entry " + journal_date)

    init_journal_entry(journal_date)

def journal_import(journal_file):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])

    # DONE Use SQLITE for the database of tweets
    # DONE write import scripts for CSV file
    # TODO Write select statements for scheduler
    # TODO create table catalogue (status text, details text, media text, tags text)

    c = conn.cursor()


    journal_dir = 'import/journal-entries/'
    # journal_file = '1917-05-04.txt'
    # create table journal_entries (journal_date text, journal_index text, journal_text text)

    file = open(journal_dir + journal_file)
    read_data = file.readlines()
    journal_date = journal_file.replace('.txt','').replace('-',' ')
    print(journal_date)
    # Delete existing rows
    c.execute('delete from journal_entries where journal_date = %s ', (journal_date,))
    conn.commit()

    warning = "WARNING!"
    ok_length = "OK"
    row_index = 0
    for row in read_data:
        row_index += 1
        journal_text = row.rstrip()
        length = len(journal_text)
        # print(journal_date, row_index,journal_text)
        print(f'{journal_date} {row_index} {journal_text} {length} ({ok_length if length < 200 else warning }) ')
        c.execute(""" INSERT INTO journal_entries (journal_date, journal_index, journal_text)
        VALUES (%s,%s,%s)""", (journal_date,row_index,journal_text))
    conn.commit()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    print(args.retrieve)
    # ready_to_write_journal()
    journal_import(args.journal)
    # get_journal_entries(args.retrieve)
    # init_journal_entry(args.retrieve)
    # print(read_journal_entry())


# --------------------------------------------------


if __name__ == '__main__':
    main()
