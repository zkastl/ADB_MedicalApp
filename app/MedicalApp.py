from datetime import datetime
from models import PatientRecord
from database import get_conn

PatientRecord.insert(first_name='Chance', last_name='Turner', age=22)

conn = get_conn()
cursor = conn.cursor()
cursor.execute('SELECT * FROM pat_record')
print(cursor.fetchall())
cursor.close()
conn.close()

today = datetime.today
#visit_list = {today: MedicalVisit(today, "Check for flu", "Achy, fever, fatigue", "Did flu test, came back negative")}
#record = PatientRecord("Zak", "Kastl", 30, visit_list)
#print(record.full_name())
#print(record.visit_history[today].visit_reason)