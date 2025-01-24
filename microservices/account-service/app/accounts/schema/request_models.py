from pydantic import BaseModel, PositiveInt
from decimal import Decimal

from app.accounts.enums import OperationType
from app.constraints import varchar_20

from app.accounts.object import IObjectData


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
