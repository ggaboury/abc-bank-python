from abcbank.transaction import Transaction
from datetime import datetime


CHECKING = 0
SAVINGS = 1
MAXI_SAVINGS = 2

class Account:
    def __init__(self, accountType):
        self.accountType = accountType
        self.transactions = []

    def deposit(self, amount):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.transactions.append(Transaction(amount))

    def withdraw(self, amount):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.transactions.append(Transaction(-amount))

    # interest earned since last transaction
    def interestEarned(self):
        amount = self.sumTransactions()
        # days since last transaction
        lasttr = self.transactions[-1].transactionDate
        td = datetime.now() - lasttr
        days = td.days

        if self.accountType == SAVINGS:
            if (amount <= 1000):
                return amount * self.compInt(0.001, days)
            else:
                return 1000 * self.compInt(0.001, days) + (amount-1000) * self.compInt(0.002, days)
        if self.accountType == MAXI_SAVINGS:
            rate = 0.05
            # date of last withdrawal
            datewds = [ t.transactionDate for t in filter(lambda x:x.amount<0, self.transactions) ]
            if len(datewds) > 0:
                delta = datetime.now() - datewds[-1]
                if delta.days <= 10:
                    rate = 0.001
            return amount * self.compInt(rate,days)
        else:
            return amount * self.compInt(0.001, days)

    def sumTransactions(self, checkAllTransactions=True):
        return sum([t.amount for t in self.transactions])
        
    @staticmethod
    def compInt(rate,days):
        dayRate = rate / 365.0
        return (1 + dayRate)**days - 1
