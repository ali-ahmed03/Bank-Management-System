# verifier.py
from z3 import *
from icontract import require

@require(lambda account_type: account_type in ("Saving", "Current"), "Invalid account type")
@require(lambda deposit: deposit >= 0, "Deposit must be non-negative")
def verifyInitialDeposit(account_type, deposit):
    s = Solver()
    acc_type = String('acc_type')
    initial_deposit = Int('initial_deposit')

    if account_type == 'Saving':
        print("[Z3] Verifying: Saving account initial deposit >= 500")
        s.add(acc_type == 'Saving', initial_deposit == deposit, initial_deposit >= 500)
    elif account_type == 'Current':
        print("[Z3] Verifying: Current account initial deposit >= 1000")
        s.add(acc_type == 'Current', initial_deposit == deposit, initial_deposit >= 1000)

    if s.check() == sat:
        print("[Z3] ✅ Verification Passed")
        return True
    else:
        print("[Z3] ❌ Verification Failed")
        return False

@require(lambda account: account is not None)
@require(lambda amount: amount > 0)
def verifySufficientFunds(account, amount):
    print(f"[Z3] Verifying: Withdrawal ≤ Balance for account {account.getAccountNo()}")
    s = Solver()
    balance = Int('balance')
    withdraw = Int('withdraw')
    s.add(balance == account.getDeposit(), withdraw == amount, balance >= withdraw)

    if s.check() == sat:
        print("[Z3] ✅ Verification Passed")
        return True
    else:
        print("[Z3] ❌ Verification Failed")
        return False

@require(lambda new_accNo: new_accNo >= 0)
@require(lambda existing_accNos: all(acc >= 0 for acc in existing_accNos))
def verifyUniqueAccountNumber(new_accNo, existing_accNos):
    print(f"[Z3] Verifying: Account number {new_accNo} is unique")

    s = Solver()
    acc = Int('acc')
    s.add(acc == new_accNo)

    for existing in existing_accNos:
        s.add(acc != existing)

    if s.check() == sat:
        print("[Z3] ✅ Account number is unique")
        return True
    else:
        print("[Z3] ❌ Duplicate account number detected")
        return False

@require(lambda account: account is not None)
@require(lambda new_type: new_type in ("Saving", "Current"))
def verifyTypeChangeFunds(account, new_type):
    deposit = account.getDeposit()
    s = Solver()
    balance = Int('balance')
    s.add(balance == deposit)

    if new_type == "Saving":
        s.add(balance >= 500)
    elif new_type == "Current":
        s.add(balance >= 1000)

    print(f"[Z3] Verifying type change from {account.type} to {new_type} with balance {deposit}")
    if s.check() == sat:
        print("[Z3] ✅ Type change allowed")
        return True
    else:
        print("[Z3] ❌ Insufficient funds for new account type")
        return False
