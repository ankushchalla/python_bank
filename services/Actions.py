from customer.Customer import CustomerService
from account.Account import AccountService
import services.Cli as Cli
from services.Cli import CustomerDetails
import logging
logger = logging.getLogger('Session')

class CreateCustomerAction:
    id = 1
    def __init__(self, customer_service: CustomerService):
        self.customer_service = customer_service

    def perform(self):
        customer_details = Cli.get_customer_details_from_input()
        generated_id = self.customer_service.create_customer(customer_details)
        print(f"Your customer_id is {generated_id}. You will need this for future logins")


    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): Create new customer")

class ViewTransactionHistoryAction:
    id = 2
    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    def perform(self):
        customer_id = Cli.get_customer_id_from_input()
        customer_accounts = self.customer_service.get_accounts_by_customer_id(customer_id)
        account_id = Cli.choose_account(customer_accounts)
        self.account_service.print_transaction_history(account_id)

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): View transaction history")

class CliSession:
    def __init__(self, session):
        self.session = session
        self.account_service = AccountService(session)
        self.customer_service = CustomerService(session)

    def start(self):
        # Print welcome
        print("CLI Bank application: Session start. Enter Q to exit")
        while True:
            # Present actions
            actions = [CreateCustomerAction, ViewTransactionHistoryAction]
            for action in actions:
                action.render_menu_item()
            
            # Map input to action requested
            action_id_requested = Cli.get_action_requested(set({CreateCustomerAction.id, ViewTransactionHistoryAction.id}))
            action_requested = self.create_action(action_id_requested)
            if action_requested is None:
                break
            
            # Service request
            action_requested.perform()

    def create_action(self, action_id: int):
        match action_id:
            case 1:
                return CreateCustomerAction(self.customer_service)
            case 2:
                return ViewTransactionHistoryAction(self.customer_service, self.account_service)
            case -1:
                print("Exiting session")
    






    


    