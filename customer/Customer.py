from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from services.Cli import Cli
from persistance.Models import Account, CustomerDetails
from persistance.Models import Customer
from account.Account import AccountService
from collections import namedtuple
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CustomerService')

class CustomerService:
    def __init__(self, session: Session):
        self.session = session
        self.account_service = AccountService(session)
        self.cli = Cli()

    def create_customer(self):
        customer_details = self.cli.get_new_customer_details()
        customer = self.__create_customer_from_input(customer_details)
        self.session.add(customer)

    def add_account(self, customer_id: int, initial_balance: float = 0.0):
        account = self.account_service.create_account(customer_id, initial_balance)
        logger.info(f"ADD_ACCOUNT_SUCCESS customer_id={customer_id} account_balance={account.balance}")

    def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = self.session.get(Customer, customer_id)
        if customer is not None:
            return customer
        else:
            raise Exception(f"CUSTOMER_NOT_FOUND customer_id={customer_id}")

    # Private methods

    def __create_customer_from_input(self, customer_details: CustomerDetails) -> Customer:
        return Customer(
            first_name=customer_details.first_name,
            last_name=customer_details.last_name,
            address=customer_details.address
        )
