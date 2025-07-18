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

    def create_customer(self, customer_details: CustomerDetails) -> int:
        customer = Customer(
            first_name = customer_details.first_name,
            last_name = customer_details.last_name,
            address = customer_details.address
        )
        self.session.add(customer)
        self.session.flush()
        logger.info(f"CREATE_CUSTOMER_SUCCESS customer_id={customer.customer_id}")
        return customer.customer_id

    def add_account(self, customer_id: int, initial_balance: float = 0.0):
        account = self.account_service.create_account(customer_id, initial_balance)
        logger.info(f"ADD_ACCOUNT_SUCCESS customer_id={customer_id} account_balance={account.balance}")

    def get_accounts_by_customer_id(self, customer_id: int) -> list[Account]:
        customer = self.get_customer_by_id(customer_id)
        return customer.accounts
    
    def customer_exists(self, customer_id: int) -> bool:
        try:
            customer = self.get_accounts_by_customer_id(customer_id)
            return True
        except:
            return False
    
    def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = self.session.get(Customer, customer_id)
        if customer is not None:
            return customer
        else:
            raise Exception(f"CUSTOMER_NOT_FOUND customer_id={customer_id}")

