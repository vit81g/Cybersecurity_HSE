import pytz
from datetime import datetime

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.history = []

    @staticmethod
    def _get_local_time():
        return pytz.utc.localize(datetime.now())

    def deposit(self, amount):
        self.balance += amount
        self.show.balance()
        self.history.append((self._get_local_time(), amount))

    def withdraw(self, amount):
        if self.balance < amount:
            self.balance -= amount
            print("Not enough balance")
            self.show.balance()
            self.history.append((self._get_local_time(), -amount))
        else:
            print("Not enough balance")
            self.show.balance()
            self.history.append((self._get_local_time(), -amount))




