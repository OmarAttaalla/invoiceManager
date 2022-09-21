class project(object):
    def __init__(self, name, date, address, payment, balance):
        self.name = name
        self.date = date
        self.address = address
        self.payment = payment
        self.balance = balance
        self.remainingBalance = balance - payment
