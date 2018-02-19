from datetime import datetime

"""
"""
class MedicalVisit(object):

    def __init__(self, visit_date=datetime.now, visit_reason="Sour Stomach", 
                 patient_comments="It hurts when I do this!", doctor_comments="Then don't do that!"):
        self.visit_date = visit_date
        self.visit_reason = visit_reason
        self.patient_comments = patient_comments
        self.doctor_comments = doctor_comments