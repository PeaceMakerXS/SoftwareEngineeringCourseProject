from .models import Account, Transaction
from abc import ABC, abstractmethod

from app.transactions.schema.request_models import CreateTransactionModel


class IAbstractFactory(ABC):
    
    @abstractmethod
    def create(data):
        raise NotImplementedError()


class CTransactionFactory(IAbstractFactory):
    
    @staticmethod
    def create(data: CreateTransactionModel) -> Transaction:
        return Transaction(**data.model_dump())