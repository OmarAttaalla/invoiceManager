from activity import activity
class project(object):
    def __init__(self, name, date, address, payment, balance, client, description, type):
        self.name = name
        self.date = date
        self.address = address
        self.payment = payment
        self.balance = balance
        self.client = client
        self.description = description
        self.activities = []
        self.type = type
        self.remainingBalance = balance - payment
    def add_activity(self, date, employee, hours, description):
        newActivity = activity(date, employee, hours, description)
        self.activities.append(newActivity)
    def render_activities(self):
        formatted_activities = []
        for activity in self.activities:
            formatted_activities.append(activity.get_array())
        return formatted_activities

