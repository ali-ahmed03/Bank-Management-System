This is a web-based Bank Management System built using Flask for the front-end interface, with formal verification integrated using the icontract library and the Z3 Theorem Prover.

Features
Create, view, modify, and delete bank accounts
Deposit and withdraw funds with validation
Interactive web interface using Bootstrap
Data stored in a simple text file (accounts.txt)

Verification
Design by Contract using icontract to enforce input/output constraints

Z3 Theorem Prover to verify:
Minimum initial deposits
Unique account numbers
Sufficient funds for withdrawal
Valid account type changes

Technologies Used:
Python 3
Flask
icontract
Z3 SMT Solver
HTML
CSS (Bootstrap)
