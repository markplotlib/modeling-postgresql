# ETL Data Modeling: *Sparkify* Streaming Music

This project builds an ETL (*extract transform load*) pipeline to perform big data operations for a fictitious streaming music app, Sparkify. This ETL pipeline uses a PostgreSQL database optimized for read queries, i.e. OLAP (Online Analytical Processing).

This ETL pipeline employs a **star schema** for the database. This star schema has a log table of `songplays` as its **fact table** at the star center. Data stored in JSON format illustrate song play data from 30 event log files, spanning the month of November 2018. This data is artificially produced using [eventsim](https://github.com/Interana/eventsim).

The **dimension tables**, situated at the star's peripheries, are tables named for `users`, `songs`, `artists`, and `time` (timestamps). This real musical data, stored in 71 JSON files, comes from the [Million Song Dataset](http://millionsongdataset.com/).


# Execution Instructions

For proper operation, these five files are to exist in the same directory. Instructions are written in the *etl.ipynb* notebook for database write operations, with prompts corresponding to read operations in *test.ipynb*.

After running code blocks in *test.ipynb*, always restart this notebook's kernel to close its database connection. This frees up exclusive access to Sparkify database, allowing *etl.ipynb* to connect.

The ETL pipeline in *etl.py* relies on the database set up done by *create_tables.py*, so please run this before running *etl.py*.

# repository files

## Python scripts

* **create_tables.py**: driver file. Defines functions to connect/disconnect to Sparkify's database, as well as to create and drop tables, calling upon table attributes found in  *sql_queries.py*. Uses *psycopg2*, a PostgreSQL database adapter for Python.

* **sql_queries.py**: CRUD operations on tables -- commands to *create*, *read*, *update* and *delete*, using SQL commands `DROP`, `INSERT`, and `SELECT`. Table attributes are defined here.

* **etl.py**: contains execution instructions identical to *etl.ipynb* in one compact script.

## Jupyter Notebook files

* **etl.ipynb**: step-by-step walkthrough to produce extract, transform, and load operations for Sparkify's database.

* **test.ipynb**: performs database reads to verify proper execution of write operations from *create_tables.py*.
