from abc import ABC, abstractmethod

from app.transactions.models import Transaction
from app.transactions.schema.request_models import CreateTransactionModel
from app.transactions.schema.response_models import GetTransactionResponse

class IAdapter(ABC):

    @staticmethod
    @abstractmethod
    def adapt(obj, **kwargs):
        raise NotImplementedError()
    

class CTransactionAdapter(IAdapter):
    
    @staticmethod
    def adapt(trans: Transaction, **kwargs) -> GetTransactionResponse:
        data = trans.get_data()
        data['sender_number'] = kwargs['sender_number']
        data['receiver_number'] = kwargs['receiver_number']
        del data['sender_id']
        del data['receiver_id']
        return GetTransactionResponse(**data)
    

class CCreateTransactionModelAdapter(IAdapter):
    @staticmethod
    def adapt(trans: CreateTransactionModel, **kwargs) -> Transaction:
        data = trans.get_data()
        data['sender_id'] = kwargs['sender_id']
        data['receiver_id'] = kwargs['receiver_id']
        del data['sender_number']
        del data['receiver_number']
        return Transaction(**data)
