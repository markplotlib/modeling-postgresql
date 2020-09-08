# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"


# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id int, start_time timestamp, 
                            user_id int, level int, song_id int, artist_id int, 
                            session_id int, location varchar , user_agent varchar);""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id int, first_name varchar, last_name varchar, 
                        gender varchar, level int);""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id int, title varchar, artist_id int, 
                        year int, duration time);""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id int, name varchar, location varchar, 
                          latitude decimal, longitude decimal);""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time timestamp, hour int, day int, week int, 
                        month int, year int, weekday bool);""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create,
                        time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
