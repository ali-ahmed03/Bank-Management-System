# account.py
from icontract import require

class Account:
    @require(lambda accNo: accNo >= 0, "Account number must be non-negative")
    @require(lambda name: isinstance(name, str) and name.strip(), "Name must be a non-empty string")
    @require(lambda acc_type: acc_type in ("Saving", "Current"), "Type must be 'Saving' or 'Current'")
    @require(lambda deposit: deposit >= 0, "Initial deposit must be non-negative")
    def __init__(self, accNo=0, name='', acc_type='', deposit=0):
        self.accNo = accNo
        self.name = name
        self.type = acc_type
        self.deposit = deposit

    @require(lambda accNo: accNo >= 0)
    @require(lambda name: isinstance(name, str) and name.strip())
    @require(lambda acc_type: acc_type in ("Saving", "Current"))
    @require(lambda deposit: deposit >= 0)
    def set_details(self, accNo, name, acc_type, deposit):
        self.accNo = accNo
        self.name = name
        self.type = acc_type
        self.deposit = deposit

    def show_details(self):
        details = (
            f"Account Number   : {self.accNo}\n"
            f"Account Holder   : {self.name}\n"
            f"Account Type     : {self.type}\n"
            f"Balance          : {self.deposit}"
        )
        return details

    @require(lambda name: isinstance(name, str) and name.strip())
    @require(lambda acc_type: acc_type in ("Saving", "Current"))
    @require(lambda deposit: deposit >= 0)
    def modify_details(self, name, acc_type, deposit):
        self.name = name
        self.type = acc_type
        self.deposit = deposit

    @require(lambda amount: amount > 0)
    def deposit_amount(self, amount):
        self.deposit += amount

    @require(lambda amount: amount > 0)
    @require(lambda self, amount: self.deposit >= amount, "Insufficient balance")
    def withdraw_amount(self, amount):
        self.deposit -= amount

    def report(self):
        return f"{self.accNo:<10}{self.name:<20}{self.type:<10}{self.deposit:<10}"

    def getAccountNo(self):
        return self.accNo

    def getDeposit(self):
        return self.deposit

    def to_file_string(self):
        return f"{self.accNo} {self.name} {self.type} {self.deposit}"

    @staticmethod
    def from_file_string(data):
        accNo, name, acc_type, deposit = data.split(' ', 3)
        return Account(int(accNo), name, acc_type, int(deposit))
