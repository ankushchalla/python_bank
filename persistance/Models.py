from sqlalchemy import Table, MetaData, String, Double, ForeignKey, create_engine, select, insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = 'customer'
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(255))
    accounts: Mapped[List["Account"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"customer_id={self.customer_id} first_name={self.first_name} last_name={self.last_name} address={self.address}"

class Account(Base):
    __tablename__ = 'account'
    account_id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(Double())
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )

    customer_id: Mapped[int] = mapped_column(ForeignKey('customer.customer_id'))
    customer: Mapped["Customer"] = relationship(back_populates="accounts")

    def withdraw(self, amount: float) -> float:
        if self.balance < amount:
            raise Exception(f"INSUFFICIENT FUNDS: current_balance={self.balance} withdraw_amount={amount}")
        self.balance = self.balance - amount
        return self.balance
    
    def deposit(self, amount: float) -> float:
        self.balance = self.balance + amount
        return self.balance

    def __repr__(self) -> str:
        return f"account_id={self.account_id} balance={self.balance} customer_id={self.customer_id}"
    
class Transaction(Base):
    __tablename__ = 'transaction'
    transaction_id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Double())
    transaction_type: Mapped[str] = mapped_column(String(30))

    account_id: Mapped[int] = mapped_column(ForeignKey('account.account_id'))
    account: Mapped["Account"] = relationship(back_populates="transactions")
