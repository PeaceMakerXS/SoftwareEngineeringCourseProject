from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories_base import BaseRepository
from .models import Account, Transaction, Currency


class AccountRepository(BaseRepository):
	_model = Account

class TransactionRepository(BaseRepository):
	_model = Transaction

	@classmethod
	async def get_deposits_by_account_number(cls, session: AsyncSession, account_number: str) -> List[Transaction] | None:
		account = (
			await session.execute(
				select(Account).where(Account.number == account_number).options(
					selectinload(Account.transactions_received)))
		).scalars().first()

		if account:
			return account.transactions_received
		else:
			return None

	@classmethod
	async def get_withdrawals_by_account_number(cls, session: AsyncSession, account_number: str) -> List[Transaction] | None:
		account = (
			await session.execute(
				select(Account).where(Account.number == account_number).options(
					selectinload(Account.transactions_sent)))
		).scalars().first()

		if account:
			return account.transactions_sent
		else:
			return None


class CurrencyRepository(BaseRepository):
	_model = Currency
