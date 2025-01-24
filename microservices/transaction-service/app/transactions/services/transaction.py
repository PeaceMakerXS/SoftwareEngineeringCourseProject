from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from typing import List

from app.unit_of_work import uow
from app.transactions.enums import OperationType, TransactionStatus
from app.transactions.repositories import AccountRepository, TransactionRepository
from app.transactions.models import Transaction
from app.transactions.schema.response_models import GetTransactionResponse
from app.transactions.schema.request_models import CreateTransactionModel

from app.transactions.adapters import CCreateTransactionModelAdapter, CTransactionAdapter

class TransactionService:

    @staticmethod
    async def get_transactions_with_account_numbers(session: AsyncSession, transactions: List[Transaction]) -> List[
        GetTransactionResponse]:
        result = []
        for transaction in transactions:
            numbers = dict()
            if transaction.sender_id:
                sender = await AccountRepository.get_by(session, id=transaction.sender_id)
                numbers['sender_number'] = sender.number
            if transaction.receiver_id:
                receiver = await AccountRepository.get_by(session, id=transaction.receiver_id)
                numbers['receiver_number'] = receiver.number

            get_transaction_response = CTransactionAdapter.adapt(transaction, **numbers)
            result.append(get_transaction_response)
        return result

    @staticmethod
    async def can_create_transaction(session: AsyncSession, data: CreateTransactionModel) -> tuple[bool, str]:
        if not await AccountRepository.exists(session, number=data.sender_number):
            return False, 'Попытка создать транзакцию от несуществующего счета.'
        if not await AccountRepository.exists(session, number=data.receiver_number):
            return False, 'Попытка создать транзакцию на несуществующий счет.'
        if data.type not in [e.value for e in OperationType]:
            return False, 'Неверный тип операции.'

        return True, ''

    @staticmethod
    def can_change_transaction_status(status: str) -> tuple[bool, str]:
        if status == TransactionStatus.CANCELLED:
            return False, 'Транзакция уже была отменена ранее.'
        elif status == TransactionStatus.SUCCESSFUL:
            return False, 'Транзакция уже была завершена.'
        return True, ''

    @staticmethod
    async def update_balance(session: AsyncSession, account_id: str, amount: Decimal):
        account = await AccountRepository.get_by(session, id=account_id)
        account.balance += amount
        await AccountRepository.update(session, account)

    @staticmethod
    async def create_transaction(data: CreateTransactionModel) -> tuple[bool, str]:
        async with uow.start() as uow_session:
            can_create, message = await TransactionService.can_create_transaction(uow_session.session, data)
            if can_create:
                sender = await AccountRepository.get_by(uow.session, number=data.sender_number)
                receiver = await AccountRepository.get_by(uow.session, number=data.receiver_number)
                ids = {'sender_id': sender.id, 'receiver_id': receiver.id}

                transaction = CCreateTransactionModelAdapter.adapt(data, **ids)
                await TransactionRepository.insert(uow_session.session, transaction)
                return True, 'Транзакция была успешно создана.'
            else:
                return False, message

    @staticmethod
    async def change_transaction_status(transaction_id: int, new_status: TransactionStatus) -> tuple[bool, str]:
        async with uow.start() as uow_session:
            transaction = await TransactionRepository.get_by(uow_session.session, id=transaction_id)
            if transaction:
                result, message = TransactionService.can_change_transaction_status(transaction.status)
                if not result:
                    return False, message

                transaction.status = new_status
                await TransactionRepository.update(uow_session.session, transaction)
                if new_status == TransactionStatus.SUCCESSFUL:
                    await TransactionService.update_balance(uow_session.session, transaction.receiver_id,
                                                            transaction.amount)
                    await TransactionService.update_balance(uow_session.session, transaction.sender_id,
                                                            -transaction.amount)
                return True, ''
            else:
                return False, f'Транзакция с id {transaction_id} не найдена.'

    @staticmethod
    async def get_account_deposits(account_number: str) -> List[GetTransactionResponse] | None:
        async with uow.start(do_commit=False) as uow_session:
            deposits = await TransactionRepository.get_deposits_by_account_number(uow_session.session, account_number)
            if deposits:
                return await TransactionService.get_transactions_with_account_numbers(uow_session.session, deposits)
            return deposits

    @staticmethod
    async def get_account_withdrawals(account_number: str) -> List[GetTransactionResponse] | None:
        async with uow.start(do_commit=False) as uow_session:
            withdrawals = await TransactionRepository.get_withdrawals_by_account_number(uow_session.session, account_number)
            if withdrawals:
                return await TransactionService.get_transactions_with_account_numbers(uow_session.session, withdrawals)
            return withdrawals
