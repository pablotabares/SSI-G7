import server as serverfunctions
import sys

if len(sys.argv) < 2:
    print('-- INSEGUS GROUP 7 BANK SERVER --')
    print('Re-run the script with one of the following options')
    print('->add (To add a new account to the system)')
    print('->install (To install the server)')
    print('->accounts (To list all saved accounts)')
    print('->transactions (To list all transactions)')
    print('->resend <account> (To resend the key via email to the customer)')
else:
    function = sys.argv[1]
    if function == 'add':
        serverfunctions.add_client()
    elif function == 'install':
        serverfunctions.initialize_db()
    elif function == 'accounts':
        serverfunctions.print_accounts()
    elif function == 'transactions':
        serverfunctions.print_transactions()
    elif function == 'resend':
        serverfunctions.resend_key(sys.argv[2])
    elif function == 'stats':
        serverfunctions.statistics()
    else:
        print('That action does not exist')
