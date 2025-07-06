# operations.py
from account import Account
from file_handler import readAllAccounts, writeAllAccounts
from verifier import verifySufficientFunds
from icontract import require

@require(lambda num: num >= 0)
@require(lambda amount: amount > 0)
@require(lambda mode: mode in ['deposit', 'withdraw'])
def deposit_or_withdraw(num, mode, amount):
    lines = readAllAccounts()
    new_lines = []
    found = False
    for line in lines:
        acc = Account.from_file_string(line)
        if acc.getAccountNo() == num:
            found = True
            if mode == 'deposit':
                acc.deposit_amount(amount)
            elif mode == 'withdraw':
                if verifySufficientFunds(acc, amount):
                    acc.withdraw_amount(amount)
                else:
                    return "insufficient"
            new_lines.append(acc.to_file_string())
        else:
            new_lines.append(line)

    if found:
        writeAllAccounts(new_lines)
        return "success"
    else:
        return "not_found"

@require(lambda num: num >= 0)
def delete_account(num):
    lines = readAllAccounts()
    new_lines = []
    found = False
    for line in lines:
        acc = Account.from_file_string(line)
        if acc.getAccountNo() != num:
            new_lines.append(line)
        else:
            found = True
    if found:
        writeAllAccounts(new_lines)
        print("Account deleted.")
    else:
        print("Account not found.")

@require(lambda current_accNo: current_accNo >= 0)
@require(lambda new_accNo: new_accNo >= 0)
@require(lambda new_name: isinstance(new_name, str) and new_name.strip())
@require(lambda new_type: new_type in ['Saving', 'Current'])
def modify_account_details_only(current_accNo, new_accNo, new_name, new_type):
    lines = readAllAccounts()
    new_lines = []
    found = False

    for line in lines:
        acc = Account.from_file_string(line)
        if acc.getAccountNo() == current_accNo:
            found = True
            acc.set_details(new_accNo, new_name, new_type, acc.getDeposit())
            new_lines.append(acc.to_file_string())
        else:
            new_lines.append(line)

    if found:
        writeAllAccounts(new_lines)
        return "success"
    else:
        return "not_found"
