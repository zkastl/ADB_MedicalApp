from datetime import datetime


class Base(object):
    __tablename__ = ''
    create_sql = ''


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
    )'''


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
    )'''