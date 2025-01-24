from pydantic import BaseModel, PositiveInt
from decimal import Decimal

from app.transactions.enums import OperationType
from app.constraints import varchar_20

from app.transactions.object import IObjectData


class CreateAccountModel(BaseModel, IObjectData):
	number: varchar_20
	balance: Decimal
	currency_id: PositiveInt | None = None

	def get_data(self):
		return {
			'number': self.number,
			'balance': self.balance,
			'currency_id': self.currency_id
		}


class CreateTransactionModel(BaseModel, IObjectData):
	amount: Decimal
	sender_number: varchar_20 | None = None
	receiver_number: varchar_20 | None = None
	type: OperationType
	mcc: int | None = None
	fee: Decimal | None = None

	def get_data(self):
		return {
			'amount': self.amount,
			'sender_number': self.sender_number,
			'receiver_number': self.receiver_number,
			'type': self.type,
			'mcc': self.mcc,
			'fee': self.fee
		}