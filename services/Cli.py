from collections import namedtuple
from persistance.Models import Account, Transaction


import logging
logger = logging.getLogger('CLI')

CustomerDetails = namedtuple('CustomerDetails', 'first_name last_name address')
        
def retry_n_times(n: int, message: str = "Error parsing input, please try again"):
    def perform(func):
        def wrapper(*args, **kwargs):
            for i in range(n + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"ACTION_FAILURE attempt_number={i + 1} exc={e}")
                    print(message)
            return Exception("Too many attempts made, terminating...")
        return wrapper
    return perform

@retry_n_times(2)
def get_action_requested(options: set[int]) -> int:
    selected_txt = input("Choose menu item by number: ")
    if selected_txt == "Q":
        return -1
    selected = int(selected_txt)
    if selected not in options:
        raise Exception(f"ACTION_ID_NOT_RECOGNIZED entered={selected} options={options}")
    return selected

@retry_n_times(2)
def get_customer_id_from_input() -> int:
    return int(input("Enter customer_id: "))

@retry_n_times(2)
def choose_account(accounts: list[Account]) -> int:
    print(f"{len(accounts)} accounts found")
    for account in accounts:
        print(account)

    return int(input("Enter account_id: "))

def print_transaction_history(transactions: list[Transaction]):
    print(f"{len(transactions)} transactions found")
    for transaction in transactions:
        print(transaction)

def get_customer_details_from_input() -> CustomerDetails:

    @retry_n_times(2)
    def get_first_name() -> str:
        return input("Enter first name: ")
    
    @retry_n_times(2)
    def get_last_name() -> str:
        return input("Enter last name: ")
    
    @retry_n_times(2)
    def get_address() -> str:
        return input("Enter address")
    
    return CustomerDetails(
        first_name = get_first_name(),
        last_name = get_last_name(),
        address = get_address()
    )





