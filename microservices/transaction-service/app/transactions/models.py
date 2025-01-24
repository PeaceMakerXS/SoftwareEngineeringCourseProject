from typing import List
from sqlalchemy import ForeignKey, String, SmallInteger, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM
from decimal import Decimal

from app.database import Base
from ..constraints import big_serial_pk, created_at, small_serial_pk
from .enums import TransactionStatus, OperationType

from app.transactions.object import IObjectData


class FinalMeta(type(Base), type(IObjectData)):
	pass

class Account(Base, IObjectData, metaclass=FinalMeta):
	__tablename__ = 'account'

	id: Mapped[big_serial_pk]
	number: Mapped[str] = mapped_column(String(20), nullable=False)
	balance: Mapped[Decimal] = mapped_column(default=0.0, nullable=False)
	currency_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('currency.id'), nullable=True)

	transactions_sent: Mapped[List['Transaction']] = relationship('Transaction', back_populates='sender',
																  uselist=True,
																  primaryjoin='Account.id==Transaction.sender_id')
	transactions_received: Mapped[List['Transaction']] = relationship('Transaction', back_populates='receiver',
																	  uselist=True,
																	  primaryjoin='Account.id==Transaction.receiver_id')
	
	def get_data(self):
		return {
			'id': self.id,
			'number': self.number,
			'balance': self.balance,
			'currency_id': self.currency_id
		}


class Transaction(Base, IObjectData, metaclass=FinalMeta):
	__tablename__ = 'transaction'

	id: Mapped[big_serial_pk]
	amount: Mapped[Decimal] = mapped_column(nullable=False)
	sender_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('account.id'), nullable=True)
	receiver_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('account.id'), nullable=True)
	time: Mapped[created_at]
	status: Mapped[TransactionStatus] = mapped_column(ENUM(TransactionStatus, name='transaction_status_enum',
														   create_type=False,
														   values_callable=lambda e: [field.value for field in e]),
													  nullable=False, default=TransactionStatus.PENDING)
	type: Mapped[OperationType] = mapped_column(ENUM(OperationType, name='operation_type_enum',
													 create_type=False,
													 values_callable=lambda e: [field.value for field in e]),
												nullable=False)
	sender_balance: Mapped[Decimal] = mapped_column(nullable=True)
	receiver_balance: Mapped[Decimal] = mapped_column(nullable=True)
	mcc: Mapped[int] = mapped_column(SmallInteger, nullable=True)
	fee: Mapped[Decimal] = mapped_column(nullable=True)

	sender: Mapped['Account'] = relationship('Account', back_populates='transactions_sent', uselist=False,
											 foreign_keys=[sender_id])
	receiver: Mapped['Account'] = relationship('Account', back_populates='transactions_received', uselist=False,
											   foreign_keys=[receiver_id])

	def get_data(self):
		return {
			'id': self.id,
			'amount': self.amount,
			'sender_id': self.sender_id,
			'receiver_id': self.receiver_id,
			'time': self.time,
			'status': self.status.value,
			'type': self.type.value,
			'sender_balance': self.sender_balance,
			'receiver_balance': self.receiver_balance,
			'mcc': self.mcc,
			'fee': self.fee
		}


class Currency(Base, IObjectData, metaclass=FinalMeta):
	__tablename__ = 'currency'

	id: Mapped[small_serial_pk]
	code: Mapped[str] = mapped_column(String(3), nullable=False)
	number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
	name: Mapped[str] = mapped_column(nullable=False)

	def get_data(self):
		return {
			'id': self.id,
			'code': self.code,
			'number': self.number,
			'name': self.name
		}
