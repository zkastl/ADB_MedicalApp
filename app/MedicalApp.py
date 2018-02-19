from datetime import datetime
from models import PatientRecord, MedicalVisit
from database import get_conn

PatientRecord.insert(first_name='Chance', last_name='Turner', age=22)
MedicalVisit.insert(visit_date=datetime.now(), visit_reason="Sour Stomach",
                 patient_comments="It hurts when I do this!", doctor_comments="Then dont do that!")

conn = get_conn()
cursor = conn.cursor()
cursor.execute('SELECT * FROM pat_record')
print(cursor.fetchall())
cursor.execute('SELECT * FROM med_visit')
print(cursor.fetchall())
cursor.close()
conn.close()

today = datetime.today
#visit_list = {today: MedicalVisit(today, "Check for flu", "Achy, fever, fatigue", "Did flu test, came back negative")}
#record = PatientRecord("Zak", "Kastl", 30, visit_list)
#print(record.full_name())
#print(record.visit_history[today].visit_reason)