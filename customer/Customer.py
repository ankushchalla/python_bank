from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from persistance.Models import Account
from persistance.Models import Customer
from account.Account import AccountService
from collections import namedtuple
from services.Cli import CustomerDetails
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CustomerService')

class CustomerService:
    def __init__(self, session: Session):
        self.session = session
        self.account_service = AccountService(session)

    def initialize(self, customer_id: int) -> Customer:
        self.customer = self.get_customer_by_id(customer_id)
        return self.customer

    def create_customer(self, customer_details: CustomerDetails) -> int:
        customer = Customer(
            first_name = customer_details.first_name,
            last_name = customer_details.last_name,
            address = customer_details.address
        )
        self.session.add(customer)
        self.session.flush()
        self.customer = customer
        logger.info(f"CREATE_CUSTOMER_SUCCESS customer_id={customer.customer_id}")
        return customer.customer_id

    def add_account(self, customer_id: int, initial_balance: float = 0.0):
        account = self.account_service.create_account(initial_balance)
        logger.info(f"ADD_ACCOUNT_SUCCESS customer_id={self.customer.customer_id} account_balance={account.balance}")

    def get_accounts(self) -> list[Account]:
        return self.customer.accounts
    
    def validate_customer_owns_account(self, account_id) -> bool:
        matched_account = [account for account in self.customer.accounts if account.account_id == account_id]
        return len(matched_account) > 0
    
    def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = self.session.get(Customer, customer_id)
        if customer is not None:
            return customer
        else:
            raise Exception(f"CUSTOMER_NOT_FOUND customer_id={customer_id}")
        
    def __str__(self) -> str:
        return f"{self.customer}"

