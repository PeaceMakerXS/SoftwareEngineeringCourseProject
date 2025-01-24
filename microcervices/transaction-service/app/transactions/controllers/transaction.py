from fastapi import APIRouter, Path
from pydantic import PositiveInt
from typing import List

from app.transactions.enums import TransactionStatus
from app.transactions.services.transaction import TransactionService
from app.transactions.schema.request_models import CreateTransactionModel
from app.transactions.schema.response_models import MessageResponse, MessageResponseWithResult, GetTransactionResponse
from .handlers_chain import Client, GetDataHandler, AccountNotExistsHandler

transaction_router = APIRouter(prefix='/transaction', tags=['Transaction API'])
client = Client()

@transaction_router.post('/new', summary='Create a new transaction',
						 response_model=MessageResponse)
async def create_transaction(data: CreateTransactionModel):
	result, message = await TransactionService.create_transaction(data)
	return {'result': result, 'message': message}


@transaction_router.put('/make_cancelled', summary='Change transaction status from "Pending" to "Cancelled"',
						response_model=MessageResponseWithResult)
async def make_transaction_cancelled(transaction_id: PositiveInt):
	result, message = await TransactionService.change_transaction_status(transaction_id, TransactionStatus.CANCELLED)
	if result:
		return {'result': True, 'message': 'Транзакция была успешно отменена.'}
	return {'result': result, 'message': message}


@transaction_router.put('/make_successful', summary='Change transaction status from "Pending" to "Successful"',
						response_model=MessageResponseWithResult)
async def make_transaction_successful(transaction_id: PositiveInt):
	result, message = await TransactionService.change_transaction_status(transaction_id, TransactionStatus.SUCCESSFUL)
	if result:
		return {'result': True, 'message': 'Транзакция была успешно завершена.'}
	return {'result': result, 'message': message}


@transaction_router.get('/get_account_withdrawals/{account_number}', summary='Get all account withdrawals',
					response_model=List[GetTransactionResponse] | MessageResponse)
async def get_account_withdrawals(account_number: str = Path(min_length=20, max_length=20)):
	client.init_handlers([GetDataHandler(([], )), AccountNotExistsHandler(account_number, not_none_values=([], ))])
	withdrawals = await TransactionService.get_account_withdrawals(account_number)
	return client.response(withdrawals, not_none_values=([], ))


@transaction_router.get('/get_account_deposits/{account_number}', summary='Get all account deposits',
					response_model=List[GetTransactionResponse] | MessageResponse)
async def get_account_deposits(account_number: str = Path(min_length=20, max_length=20)):
	client.init_handlers([GetDataHandler(([], )), AccountNotExistsHandler(account_number, not_none_values=([], ))])
	deposits = await TransactionService.get_account_deposits(account_number)
	return client.response(deposits, not_none_values=([], ))