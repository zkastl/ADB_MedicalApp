from models import MedicalVisit, PatientRecord
from database import reset_db, copy_table_to_col_version
from faker import Faker
import random
from datetime import timedelta, datetime

factory = Faker()

clear_data_first = False
num_of_groups = 10000
num_in_group = 100


def add_patient_record(records):
    first_name, last_name = tuple(factory.name().split(' ')[:2])
    statement = ''
    for i in range(records):
        statement += PatientRecord.gen_insert_sql(
            first_name=first_name,
            last_name=last_name,
            age=random.randint(18, 95)
        )
    PatientRecord.run_sql(statement)


def add_medical_visit(records):
    statement = ''
    for i in range(records):
        statement += MedicalVisit.gen_insert_sql(
            visit_date=random_date(
                start=datetime.utcfromtimestamp(157766400),
                end=datetime.utcnow()
            ),
            visit_reason=factory.text(900),
            patient_comments=factory.text(900),
            doctor_comments=factory.text(900)
        )
    MedicalVisit.run_sql(statement)


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


if __name__ == '__main__':
    if clear_data_first:
        reset_db()

    for i in range(num_of_groups):
        if i % 10 == 0:
            print('Record number: ' + str(i*num_in_group))
        add_patient_record(num_in_group)
        add_medical_visit(num_in_group)

    copy_table_to_col_version(MedicalVisit.__tablename__)
    copy_table_to_col_version(PatientRecord.__tablename__)
