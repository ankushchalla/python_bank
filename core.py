# -*- coding: utf-8 -*-
from customer.Customer import CustomerService
from account.Account import AccountService

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/bank')
with Session(engine) as session:
    customer_service = CustomerService(session)
    customer = customer_service.create_customer()
    session.commit()


