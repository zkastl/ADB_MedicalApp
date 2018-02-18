"""
"""
class PatientRecord(object):

    def __init__(self, first_name="John", last_name="Doe", age=0, visit_history=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.visit_history = visit_history

    def full_name(self):
        return self.first_name + " " + self.last_name