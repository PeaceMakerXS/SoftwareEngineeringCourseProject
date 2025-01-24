from pydantic import BaseModel, ConfigDict, PositiveInt
from datetime import datetime
from decimal import Decimal

from app.constraints import varchar_20
from app.transactions.enums import TransactionStatus, OperationType

from app.transactions.object import IObjectData


class GetTransactionResponse(BaseModel, IObjectData):
	model_config = ConfigDict(from_attributes=True)

	id: PositiveInt
	amount: Decimal
	sender_number: varchar_20 | None = None
	receiver_number: varchar_20 | None = None
	time: datetime
	status: TransactionStatus
	type: OperationType
	sender_balance: Decimal | None = None
	receiver_balance: Decimal | None = None
	mcc: int | None = None
	fee: Decimal | None = None

	def get_data(self):
		return {
			'id': self.id,
			'amount': self.amount,
			'time': self.time,
			'status': self.status.value,
			'type': self.type.value,
			'sender_balance': self.sender_balance,
			'receiver_balance': self.receiver_balance,
			'mcc': self.mcc,
			'fee': self.fee
		}


class MessageResponse(BaseModel, IObjectData):
	message: str

	def get_data(self):
		return {
			'message': self.message,
		}


class MessageResponseWithResult(BaseModel, IObjectData):
	result: bool
	message: str

	def get_data(self):
		return {
			'result': self.result,
			'message': self.message
		}
