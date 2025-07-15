# -*- coding: utf-8 -*-
from customer.Customer import CustomerService
from account.Account import AccountService

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/bank')
with Session(engine) as session:
    account_service = AccountService(session)
    account_service.withdraw(10, 10.0)
    account_service.deposit(1, 10.0)
    account_service.withdraw(1, 20.0)
    session.commit()


