# Command for Docker to setup database
# docker run --name postgres -p 5432:5432 -d postgres:10

# For column and row oriented in one
# docker run --name column -p 5432:5432 -d simpleman19/columndb
# docker exec -it column /bin/bash
# Run command: echo "shared_preload_libraries = 'cstore_fdw'" >> /var/lib/postgresql/data/postgresql.conf
# Exit
# docker restart column

# After running docker command run this python file to create/reset DB with tables

import psycopg2
import sys
import inspect

# Define our connection string
conn_string = "host='localhost' dbname='postgres' user='postgres' password='secret'"

last_names = [
    'Pineda',
    'Patel',
    'Gould',
    'Orozco',
    'Stanley',
    'Johnson',
    'Chan',
    'Gaines',
    'Goodman',
    'Wilkerson',
    'Allen',
    'Lucas',
    'Krause',
    'Gonzalez',
    'Summers',
    'Jefferson',
    'Singh',
    'Barry',
    'Murphy',
    'Mays'
    ]

first_names = [
    'Zaid',
    'Callum',
    'Jeff',
    'Ezeqiel',
    'Juan',
    'Giovanni',
    'Johan',
    'Pedro'
    'Raiden',
    'Sage',
    'Scott',
    'Aiyana',
    'Ariel',
    'Ivy',
    'Krista',
    'Lillie',
    'Litzy',
    'Aliza',
    'Sierra',
    'Dixie',
    'Salma',
    'Janae',
    'Itzel'
    ]


def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    import models
    for name, cls in models.__dict__.items():
        if inspect.isclass(cls):
            if issubclass(cls, models.Base) and name != 'Base':
                print('Found Model: ' + name)
                cursor.execute(cls.create_sql)
                cursor.execute(cls.create_column_sql)
    conn.commit()
    cursor.execute('SELECT show_tables()')
    ret = cursor.fetchall()
    print('Created: ' + str(ret))
    for table in ret:
        print('Table: ' + table[0].split('.')[1])
        cursor.execute('SELECT * from describe_table(\'' + table[0].split('.')[1] + '\')')
        print(cursor.fetchall())
    cursor.close()
    conn.close()


def drop_db():
    conn = get_conn()
    cursor = conn.cursor()
    conn.commit()
    cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;')
    conn.commit()
    cursor.execute('''create or replace function show_tables() returns SETOF text as $$
                    SELECT
                        table_schema || '.' || table_name as show_tables
                    FROM
                        information_schema.tables
                    WHERE
                        table_type = 'BASE TABLE'
                    AND
                        table_schema NOT IN ('pg_catalog', 'information_schema');
                    $$
                    language sql; '''
                   )
    cursor.execute('''create or replace function describe_table(tbl_name text) returns table(column_name   
                    varchar, data_type varchar,character_maximum_length int) as $$
                    select column_name, data_type, character_maximum_length
                    from INFORMATION_SCHEMA.COLUMNS where table_name = $1;
                    $$
                    language 'sql';
                    ''')
    conn.commit()
    cursor.close()
    conn.close()


def reset_db():
    drop_db()
    setup_column_server()
    init_db()


def setup_column_server():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('''
                        CREATE EXTENSION cstore_fdw;
                        CREATE SERVER cstore_server FOREIGN DATA WRAPPER cstore_fdw;
                    '''
                   )
    conn.commit()
    cursor.close()
    conn.close()


def copy_table_to_col_version(table):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ' + table + '_col SELECT * FROM ' + table + ';')
    conn.commit()
    cursor.close()
    conn.close()


def get_conn():
    conn = psycopg2.connect(conn_string)
    return conn


def make_records():
    from models import PatientRecord
    import random
    for i in range(1000):
        PatientRecord.insert(first_name=random.choice(first_names), last_name=random.choice(last_names), age=random.randint(5,90))


if __name__ == '__main__':
    reset_db()
    make_records()