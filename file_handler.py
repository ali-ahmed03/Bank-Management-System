import os
from icontract import ensure, require

def writeAccountToFile(account):
        with open('accounts.txt', 'a' if os.path.exists("accounts.txt") else 'w') as file:
            file.write(account.to_file_string() + '\n')

@ensure(lambda result: isinstance(result, list))
def readAllAccounts():
        if not os.path.exists("accounts.txt"):
            return []
        with open('accounts.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

@require(lambda lines: isinstance(lines, list))
def writeAllAccounts(lines):
        with open('accounts.txt', 'w') as file:
            file.writelines([line + '\n' for line in lines])
