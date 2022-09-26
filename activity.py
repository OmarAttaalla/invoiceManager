class activity(object):
    def __init__(self, date, employee, hours, description):
        self.date = date
        self.employee = employee
        self.hours = hours
        self.description = description
    def get_array(self):
        return [self.date, self.employee, self.hours, self.description]
