from app.repositories_base import BaseRepository
from .models import Account, Currency


class AccountRepository(BaseRepository):
	_model = Account

class CurrencyRepository(BaseRepository):
	_model = Currency
