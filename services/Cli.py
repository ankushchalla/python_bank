from collections import namedtuple
from persistance.Models import CustomerDetails
from persistance.Models import Account, Transaction

import logging
logger = logging.getLogger('CLI')
        
def perform_n_times(n: int, message: str = "Error parsing input, please try again"):
    def perform(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"ACTION_FAILURE attempt_number={i + 1} exc={e}")
                    print(message)
            return Exception("Too many attempts made, terminating...")
        return wrapper
    return perform

@perform_n_times(3)
def get_customer_id_from_input() -> int:
    return int(input("Enter customer_id: "))

@perform_n_times(3)
def choose_account(accounts: list[Account]) -> int:
    print(f"{len(accounts)} accounts found")
    for account in accounts:
        print(account)

    return int(input("Enter account_id: "))

def print_transaction_history(transactions: list[Transaction]):
    print(f"{len(transactions)} transactions found")
    for transaction in transactions:
        print(transaction)





