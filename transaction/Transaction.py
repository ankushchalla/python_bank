from functools import wraps
from sqlalchemy.orm import Session
from persistance.Models import Transaction
import logging
logger = logging.getLogger('Transaction')

class TransactionService:
    def __init__(self, session: Session):
        self.session = session

    def record_transaction(self, account_id: int, amount: float, transaction_type: str):
        transaction = Transaction(
            amount = amount,
            account_id = account_id,
            transaction_type = transaction_type
        )
        self.session.add(transaction)

