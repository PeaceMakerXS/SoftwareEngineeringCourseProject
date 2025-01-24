from pydantic import BaseModel, ConfigDict, PositiveInt
from datetime import datetime
from decimal import Decimal

from app.constraints import varchar_20
from app.accounts.enums import TransactionStatus, OperationType

from app.accounts.object import IObjectData


class GetAccountResponse(BaseModel, IObjectData):
	model_config = ConfigDict(from_attributes=True)

	id: PositiveInt
	number: str
	balance: Decimal
	currency_id: PositiveInt

	def get_data(self):
		return {
			'id': self.id,
			'number': self.number,
			'balance': self.balance,
			'currency_id': self.currency_id
		}


class MessageResponse(BaseModel, IObjectData):
	message: str

	def get_data(self):
		return {
			'message': self.message,
		}
