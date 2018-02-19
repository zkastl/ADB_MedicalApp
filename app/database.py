# Command for Docker to setup database
# docker run --name postgres -p 5432:5432 -d postgres:10
# After running docker command run this python file to create/reset DB with tables

import psycopg2
import sys
import inspect

# Define our connection string
conn_string = "host='localhost' dbname='postgres' user='postgres' password='secret'"


def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    import models
    for name, cls in models.__dict__.items():
        if inspect.isclass(cls):
            if issubclass(cls, models.Base) and name != 'Base':
                print('Found Model: ' + name)
                cursor.execute(cls.create_sql)
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
    init_db()


def get_conn():
    conn = psycopg2.connect(conn_string)
    return conn


if __name__ == '__main__':
    reset_db()