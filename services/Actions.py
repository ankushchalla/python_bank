from customer.Customer import CustomerService
from account.Account import AccountService
import services.Cli as Cli
from functools import reduce
import logging
logger = logging.getLogger('Session')

class LoginAction:
    id = 1
    customer_is_logged_in = False

    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    def perform(self):
        customer_id = Cli.get_customer_id_from_input()
        customer = self.customer_service.initialize(customer_id)
        self.account_service.initialize(customer)
        LoginAction.customer_is_logged_in = True
        print(f"Login successful. Welcome {self.customer_service}\n")

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): Login")

class CreateCustomerAction:
    id = 2

    def __init__(self, customer_service: CustomerService):
        self.customer_service = customer_service

    def perform(self):
        customer_details = Cli.get_customer_details_from_input()
        generated_id = self.customer_service.create_customer(customer_details)
        print(f"Your customer_id is {generated_id}. You will need this for future logins\n")

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): Create new customer")

class ViewTransactionHistoryAction:
    id = 3

    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    @Cli.retry_n_times(2, "Please enter a different account_id")
    def perform(self):
        customer_accounts = self.customer_service.get_accounts()
        account_id = Cli.choose_account(customer_accounts)
        customer_owns_account = self.customer_service.validate_customer_owns_account(account_id)
        if not customer_owns_account:
            raise Exception(f"account with account_id {account_id} not found. Please enter a different account_id")
        
        self.account_service.print_transaction_history(account_id)

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): View transaction history")

class CreateAccountAction:
    id = 4

    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    def perform(self):
        account_details = Cli.get_account_details_from_input()
        account = self.account_service.create_account(initial_balance=account_details.initial_balance)
        print(f"Created account: {account}\n")

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): Create a new account")

class DepositAction:
    id = 5

    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    @Cli.retry_n_times(2, "Please enter a different account_id")
    def perform(self):
        customer_accounts = self.customer_service.get_accounts()
        account_id = Cli.choose_account(customer_accounts)
        customer_owns_account = self.customer_service.validate_customer_owns_account(account_id)
        if not customer_owns_account:
            raise Exception(f"account with account_id {account_id} not found. Please enter a different account_id")
        
        deposit_amount = Cli.get_amount_from_input("Deposit amount: ")
        deposit_successful = self.account_service.deposit(account_id, deposit_amount)
        if deposit_successful:
            print(f"Successfully deposited ${deposit_amount}\n")
        else:
            print(f"Failed to deposit ${deposit_amount}. Please try again another time.\n")
        

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): Make a deposit")

class WithdrawAction:
    id = 6

    def __init__(self, customer_service: CustomerService, account_service: AccountService):
        self.customer_service = customer_service
        self.account_service = account_service

    @Cli.retry_n_times(2, "Please enter a different account_id")
    def perform(self):
        customer_accounts = self.customer_service.get_accounts()
        account_id = Cli.choose_account(customer_accounts)
        customer_owns_account = self.customer_service.validate_customer_owns_account(account_id)
        if not customer_owns_account:
            raise Exception(f"account with account_id {account_id} not found.")
        
        withdraw_amount = Cli.get_amount_from_input("Withdraw amount: ")
        withdraw_successful = self.account_service.withdraw(account_id, withdraw_amount)
        if withdraw_successful:
            print(f"Successfully withdrawed ${withdraw_amount}\n")
        else:
            print(f"Failed to withdraw ${withdraw_amount}.\n")
        

    @classmethod
    def render_menu_item(cls):
        print(f"({cls.id}): Withdraw")

class CliSession:
    def __init__(self, session):
        self.session = session
        self.account_service = AccountService(session)
        self.customer_service = CustomerService(session)

    def start(self):
        # Print welcome
        print("\nCLI Bank application: Session start. Enter Q to exit")
        while True:
            # Present actions
            if not LoginAction.customer_is_logged_in:
                actions = [LoginAction, CreateCustomerAction]
            else:
                actions = [ViewTransactionHistoryAction, CreateAccountAction, DepositAction, WithdrawAction]
            for action in actions:
                action.render_menu_item()
            
            # Map input to action requested
            options = [action.id for action in actions]
            action_id_requested = Cli.get_action_requested(set(options))
            action_requested = self.create_action(action_id_requested)
            if action_requested is None:
                break
            
            # Service request
            action_requested.perform()

    def create_action(self, action_id: int):
        match action_id:
            case LoginAction.id:
                return LoginAction(self.customer_service, self.account_service)
            case CreateCustomerAction.id:
                return CreateCustomerAction(self.customer_service)
            case ViewTransactionHistoryAction.id:
                return ViewTransactionHistoryAction(self.customer_service, self.account_service)
            case CreateAccountAction.id:
                return CreateAccountAction(self.customer_service, self.account_service)
            case DepositAction.id:
                return DepositAction(self.customer_service, self.account_service)
            case WithdrawAction.id:
                return WithdrawAction(self.customer_service, self.account_service)
            case -1:
                print("Exiting session")
    






    


    