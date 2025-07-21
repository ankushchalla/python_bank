from sqlalchemy import  insert, create_engine, text, select
from sqlalchemy.orm import Session
from persistance.Models import Customer, Account
from transaction.Transaction import TransactionService
from typing import List
from functools import reduce
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('AccountService')

class AccountService:
    def __init__(self, session: Session):
        self.session = session
        self.transaction_service = TransactionService(session)

    def initialize(self, customer: Customer):
        self.customer = customer

    def create_account(self, initial_balance: float = 0.0) -> Account:
        account = Account(customer_id=self.customer.customer_id, balance=initial_balance)
        self.session.add(account)
        self.session.flush()
        return account
    
    def withdraw(self, account_id: int, transaction_amount: float) -> bool:
        try: 
            account = self.get_account_by_id(account_id)
            new_balance = account.withdraw(transaction_amount)
            self.transaction_service.record_transaction(account_id, transaction_amount, 'WITHDRAWAL')
            logger.info(f"WITHDRAW_SUCCESS new_balance=${new_balance}")
            return True
        except Exception as e:
            logger.error(f"WITHDRAW_FAILURE account_id={account_id} exc={e}")
            return False

    def deposit(self, account_id: int, transaction_amount: float) -> bool:
        try:
            account = self.get_account_by_id(account_id)
            new_balance = account.deposit(transaction_amount)
            self.transaction_service.record_transaction(account_id, transaction_amount, 'DEPOSIT')
            logger.info(f"DEPOSIT_SUCCESS new_balance=${new_balance}")
            return True
        except Exception as e:
            logger.error(f"DEPOSIT_FAILURE account_id={account_id} exc={e}")
            return False

    def print_transaction_history(self, account_id: int):
        try:
            account = self.get_account_by_id(account_id)
            print(f"{len(account.transactions)} transactions found")
            for transaction in account.transactions:
                print(transaction)
        except Exception as e:
            logger.error(f"TXN_READ_FAILURE account_id={account_id} exc={e}")
        
    def get_account_by_id(self, account_id: int) -> Account:
        account = self.session.get(Account, account_id)
        if account is not None:
            return account
        else:
            raise Exception(f"ACCOUNT_NOT_FOUND account_id={account_id}")
    
            
        
    
    
