# app.py (Flask main file)
from flask import Flask, render_template, request, redirect, flash, url_for
from account import Account
from operations import deposit_or_withdraw, delete_account, modify_account_details_only
from verifier import verifyInitialDeposit, verifyUniqueAccountNumber, verifyTypeChangeFunds
from file_handler import writeAccountToFile, readAllAccounts

app = Flask(__name__)
app.secret_key = 'bank_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        accNo = int(request.form['accNo'])
        name = request.form['name']
        acc_type = request.form['acc_type'].capitalize()
        deposit = int(request.form['deposit'])

        lines = readAllAccounts()
        existing_accNos = [Account.from_file_string(line).getAccountNo() for line in lines]

        if not verifyUniqueAccountNumber(accNo, existing_accNos):
            flash('Duplicate account number!', 'danger')
        elif not verifyInitialDeposit(acc_type, deposit):
            flash('Initial deposit does not meet minimum requirement!', 'danger')
        else:
            try:
                account = Account(accNo, name, acc_type, deposit)
                writeAccountToFile(account)
                flash('Account created successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(str(e), 'danger')

    return render_template('create_account.html')

@app.route('/deposit_withdraw', methods=['GET', 'POST'])
def deposit_withdraw():
    if request.method == 'POST':
        accNo = int(request.form['accNo'])
        amount = int(request.form['amount'])
        action = request.form['action']

        try:
            status = deposit_or_withdraw(accNo, action, amount)
            if status == 'success':
                flash(f"{amount} {action}ed successfully!", 'success')
            elif status == 'not_found':
                flash("Account not found!", 'danger')
            elif status == 'insufficient':
                flash("Insufficient funds!", 'danger')
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('deposit_withdraw.html')

@app.route('/accounts')
def all_accounts():
    accounts = [Account.from_file_string(line) for line in readAllAccounts()]
    return render_template('accounts.html', accounts=accounts)

@app.route('/delete/<int:accNo>')
def delete(accNo):
    delete_account(accNo)
    flash(f"Account {accNo} deleted.", 'info')
    return redirect(url_for('all_accounts'))

@app.route('/modify/<int:accNo>', methods=['GET', 'POST'])
def modify(accNo):
    account = None
    lines = readAllAccounts()
    for line in lines:
        acc = Account.from_file_string(line)
        if acc.getAccountNo() == accNo:
            account = acc
            break

    if not account:
        flash("Account not found.", 'danger')
        return redirect(url_for('all_accounts'))

    if request.method == 'POST':
        new_accNo = int(request.form['accNo'])
        new_name = request.form['name']
        new_type = request.form['acc_type'].capitalize()

        # Ensure uniqueness only if account number is changed
        if new_accNo != accNo:
            existing_accNos = [Account.from_file_string(line).getAccountNo() for line in lines if Account.from_file_string(line).getAccountNo() != accNo]
            if not verifyUniqueAccountNumber(new_accNo, existing_accNos):
                flash('Duplicate account number!', 'danger')
                return render_template('modify_account.html', account=account)

        if not verifyTypeChangeFunds(account, new_type):
            flash(f"Insufficient funds for {new_type} account!", 'danger')
        else:
            status = modify_account_details_only(acc.getAccountNo(), new_accNo, new_name, new_type)
            if status == 'success':
                flash("Account modified successfully!", 'success')
                return redirect(url_for('all_accounts'))
            else:
                flash("Failed to modify account.", 'danger')

    return render_template('modify_account.html', account=account)

if __name__ == '__main__':
    app.run(debug=True)