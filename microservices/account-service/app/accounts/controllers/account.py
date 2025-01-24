from typing import Union, List
from fastapi import APIRouter, Path

from app.accounts.services.account import AccountService
from app.accounts.schema.request_models import CreateAccountModel
from app.accounts.schema.response_models import GetAccountResponse, MessageResponse
from .handlers_chain import (AccountNotExistsHandler, AccountAlreadyExistsHandler, AccountCreatingHandler,
							 AccountDeletingHandler, GetDataHandler, Client)

account_router = APIRouter(prefix='/account', tags=['Account API'])
client = Client()

@account_router.post('/new', summary='Create a new account',
					 response_model=MessageResponse)
async def create_account(data: CreateAccountModel):
	client.init_handlers([AccountCreatingHandler(data.number), AccountAlreadyExistsHandler(data.number)])
	has_created = await AccountService.create_account(data)
	return client.response(has_created)


@account_router.delete('/delete/{account_number}', summary='Delete account by number',
					 response_model=MessageResponse)
async def delete_account(account_number: str = Path(min_length=20, max_length=20)):
	client.init_handlers([AccountDeletingHandler(account_number), AccountNotExistsHandler(account_number)])
	has_deleted = await AccountService.delete_account(account_number)
	return client.response(has_deleted)


@account_router.get('/get_all', summary='Get all accounts',
					response_model=List[GetAccountResponse])
async def get_all_accounts():
	client.init_handlers([GetDataHandler(([], ))])
	accounts = await AccountService.get_all_accounts()
	return client.response(accounts, not_none_values=([], ))


@account_router.get('/get_account/{account_number}', summary='Get account by number',
					response_model=Union[GetAccountResponse, MessageResponse])
async def get_account(account_number: str = Path(min_length=20, max_length=20)):
	client.init_handlers([GetDataHandler(), AccountNotExistsHandler(account_number)])
	account = await AccountService.get_account(account_number)
	return client.response(account)
