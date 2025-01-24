from abc import ABC, abstractmethod
from typing import List, Any

class DataHandler(ABC):
	@abstractmethod
	def convert_to_response(self, data_to_handle):
		raise NotImplementedError()

class AccountHandler(object):
	not_none_values = ()

	def __init__(self, account_number: str, not_none_values=()):
		self.account_number = account_number
		self.not_none_values = not_none_values


class AccountNotExistsHandler(DataHandler, AccountHandler):
	def convert_to_response(self, data_to_handle):
		if not data_to_handle and data_to_handle not in self.not_none_values:
			return {'message': f'Аккаунт с номером {self.account_number} не найден.'}


class GetDataHandler(DataHandler):
	not_none_values = ()

	def __init__(self, non_non_values=()):
		self.not_none_values = non_non_values

	def convert_to_response(self, data_to_handle):
		if data_to_handle or data_to_handle in self.not_none_values:
			return data_to_handle


class Client(object):
	def __init__(self):
		self._handlers = []

	def add_handler(self, h):
		self._handlers.append(h)

	def init_handlers(self, handlers: List[Any]):
		self._handlers = handlers

	def response(self, data_to_handle, not_none_values=()):
		for h in self._handlers:
			resp = h.convert_to_response(data_to_handle)
			if resp or resp in not_none_values:
				return resp
		else:
			return {'message': 'Неизвестная ошибка.'}
