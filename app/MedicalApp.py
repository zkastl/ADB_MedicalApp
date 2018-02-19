from datetime import datetime
from app.PatientRecord import PatientRecord
from app.MedicalVisit import MedicalVisit

today = datetime.today
visit_list = {today: MedicalVisit(today, "Check for flu", "Achy, fever, fatigue", "Did flu test, came back negative")}
record = PatientRecord("Zak", "Kastl", 30, visit_list)
print(record.full_name())
print(record.visit_history[today].visit_reason)