# -*- coding: utf-8 -*-
from customer.Customer import CustomerService
from account.Account import AccountService
from services.Actions import ViewTransactionHistoryAction

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('mysql+mysqldb://root:password@localhost:3306/bank')
with Session(engine) as session:
    customer_service = CustomerService(session)
    account_service = AccountService(session)
    action = ViewTransactionHistoryAction(customer_service, account_service)
    action.perform()


