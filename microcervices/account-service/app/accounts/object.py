from abc import ABC, abstractmethod


class IObjectData(ABC):
    @abstractmethod
    def get_data(self):
        raise NotImplementedError()
