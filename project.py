class project(object):
    def __init__(self, name, date, address, payment, balance, client, notes):
        self.name = name
        self.date = date
        self.address = address
        self.payment = payment
        self.balance = balance
        self.client = client
        self.notes = notes
        self.remainingBalance = balance - payment
