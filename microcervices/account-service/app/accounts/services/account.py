from typing import List

from app.unit_of_work import uow
from app.accounts.models import Account
from app.accounts.repositories import AccountRepository
from app.accounts.schema.request_models import CreateAccountModel

from app.accounts.factories import CAccountFactory

class AccountService:

	@staticmethod
	async def create_account(data: CreateAccountModel) -> bool:
		async with uow.start() as uow_session:
			account = CAccountFactory.create(data)
			if not await AccountRepository.exists(uow_session.session, number=account.number):
				await AccountRepository.insert(uow_session.session, account)
				return True
			else:
				return False

	@staticmethod
	async def delete_account(account_number: str) -> bool:
		async with uow.start() as uow_session:
			account = await AccountRepository.get_by(uow_session.session, number=account_number)
			if account:
				await AccountRepository.delete_object(uow_session.session, account)
				return True
			else:
				return False

	@staticmethod
	async def get_all_accounts() -> List[Account]:
		async with uow.start(do_commit=False) as uow_session:
			return await AccountRepository.find_all(uow_session.session)

	@staticmethod
	async def get_account(account_number: str) -> Account | None:
		async with uow.start(do_commit=False) as uow_session:
			return await AccountRepository.get_by(uow_session.session, number=account_number)
