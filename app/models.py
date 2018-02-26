from datetime import datetime
from database import get_conn


class Base(object):
    __tablename__ = ''
    create_sql = ''

    @classmethod
    def insert(cls, **kwargs):
        statement = cls.gen_insert_sql(**kwargs)
        cls.run_sql(statement)

    @classmethod
    def run_sql(cls, statement):
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(statement)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def gen_insert_sql(cls, **kwargs):
        statement = 'INSERT INTO ' + cls.__tablename__ + '('
        for key, value in kwargs.items():
            statement += key + ', '
        statement = statement[:-2]
        statement += ') VALUES('
        for key, value in kwargs.items():
            if type(value).__name__ == 'int':
                statement += str(value) + ', '
            elif type(value).__name__ == 'datetime.datetime':
                statement += str(value) + ', '
            else:
                statement += '\'' + str(value) + '\', '
        statement = statement[:-2]
        statement += ');'
        return statement


class MedicalVisit(Base):
    __tablename__ = 'med_visit'

    def __init__(self, visit_date=datetime.now, visit_reason="Sour Stomach",
                 patient_comments="It hurts when I do this!", doctor_comments="Then don't do that!"):
        self.visit_date = visit_date
        self.visit_reason = visit_reason
        self.patient_comments = patient_comments
        self.doctor_comments = doctor_comments

    create_sql = 'CREATE TABLE ' + __tablename__ + '''(
    id  SERIAL PRIMARY KEY NOT NULL,
    visit_date  TIMESTAMP,
    visit_reason VARCHAR(1000),
    patient_comments VARCHAR(1000),
    doctor_comments VARCHAR(1000)
    );'''
    create_column_sql = create_colunn_sql = 'CREATE FOREIGN TABLE ' + __tablename__ + '''_col(
    id INT,
    visit_date  TIMESTAMP,
    visit_reason VARCHAR(1000),
    patient_comments VARCHAR(1000),
    doctor_comments VARCHAR(1000)
    )
    SERVER cstore_server
    OPTIONS(compression 'pglz');
    '''


class PatientRecord(Base):
    __tablename__ = 'pat_record'

    def __init__(self, first_name="John", last_name="Doe", age=0):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def full_name(self):
        return self.first_name + " " + self.last_name

    create_sql = 'CREATE TABLE ' + __tablename__ + '''(
    id  SERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(1000),
    last_name VARCHAR(1000),
    age INTEGER
    );'''

    create_column_sql = 'CREATE FOREIGN TABLE ' + __tablename__ + '''_col(
    id INT,
    first_name VARCHAR(1000),
    last_name VARCHAR(1000),
    age INTEGER
    )
    SERVER cstore_server
    OPTIONS(compression 'pglz');
    '''