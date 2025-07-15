from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from persistance.Models import Account
from persistance.Models import Customer
import logging

class CustomerService:
    def __init__(self, session: Session):
        self.session = session
