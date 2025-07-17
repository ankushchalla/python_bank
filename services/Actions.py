from customer.Customer import CustomerService
from account.Account import AccountService
import services.Cli as Cli


import logging
logger = logging.getLogger('Session')

class ViewTransactionHistoryAction:
    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    def perform(self):
        customer_id = Cli.get_customer_id_from_input()
        customer_accounts = self.customer_service.get_accounts_by_customer_id(customer_id)
        account_id = Cli.choose_account(customer_accounts)
        self.account_service.print_transaction_history(account_id)

    def __str__(self) -> str:
        return "(1): View transaction history"

class CliSession:
    def __init__(self, session):
        self.session = session
        self.account_service = AccountService(session)
        self.customer_service = CustomerService(session)

    def start(self):
        # Print welcome
        print("CLI Bank application: Session start.")

        # # Present actions
        # for action in actions:
        #     print(action)
        
        # action_requested = get_action_requested()
        
        # # Service request
        # service_request(action_requested)

    






    


    