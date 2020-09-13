import os
import glob
import psycopg2
import pandas as pd
import datetime

from sql_queries import *


def run_sample_query(cur):
    """
    Performs a simplified query over the larger data set.

    :param cur: cursor object for PostgreSQL command execution in Python
    :return: results of query
    """
    # Since this is a subset of the much larger dataset,
    # the solution dataset will only have 1 row with values
    return cur.execute(sample_query)


def process_song_file(cur, filepath):
    """
    Performs ETL processes to construct dimension tables of songs and artists.

    :param cur: cursor object for PostgreSQL command execution in Python
    :param filepath: string file name and directory
    :return: none
    """""
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id',
                         'year', 'duration']].values)
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location',
                           'artist_latitude', 'artist_longitude']])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Performs ETL processes to construct fact table of songplays,
    and dimension tables of users and time.

    :param cur: cursor object for PostgreSQL command execution in Python
    :param filepath: string file name and directory
    :return: none
    """""

    # open log file
    df = pd.read_json(filepath, lines=True)

    # convert timestamp column to datetime
    df['dt'] = list(map(datetime.datetime.fromtimestamp, df.loc[:,'ts']/1E3))
    # filter by NextSong action
    df = df[df['page']=='NextSong']
    t = df['dt'].dt
    # df = df[df['page']=='NextSong']
    # t = list(map(datetime.datetime.fromtimestamp, df.loc[:,'ts']/1E3)).dt

    # insert time data records
    time_data = list([df['ts'], t.hour, t.day, t.weekofyear,
                      t.month, t.year, t.weekday])
    column_labels = ('start_time', 'hour', 'day', 'weekofyear',
                     'month', 'year', 'weekday')

    d = dict()
    for i, col in enumerate(column_labels):
        d[col] = time_data[i]

    time_df = pd.DataFrame(d)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get song_id and artist_id from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        song_id, artist_id = results if results else None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, song_id, artist_id,
                         row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    :param cur: cursor object for PostgreSQL command execution in Python
    :param conn: database connection object
    :param filepath: string file name and directory
    :param func: callable, to process file
    :return: none
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Creates sparkify database, establishing connection
    to build ETL pipeline and run OLAP.

    :return: none
    """

    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    sample = input("Run sample query? (Y/n) ")
    if sample.lower() != "n":
        sample_results = run_sample_query(cur)
        print(sample_query, "\n")
        print(sample_results)

    conn.close()


if __name__ == "__main__":
    main()
