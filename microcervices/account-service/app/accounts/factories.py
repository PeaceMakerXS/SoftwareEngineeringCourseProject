from .models import Account, Transaction
from abc import ABC, abstractmethod

from app.accounts.schema.request_models import CreateAccountModel


class IAbstractFactory(ABC):
    
    @abstractmethod
    def create(data):
        raise NotImplementedError()
    

class CAccountFactory(IAbstractFactory):
    
    @staticmethod
    def create(data: CreateAccountModel) -> Account:
        return Account(**data.model_dump())
