from abc import ABC, abstractmethod

class DissertationRepositoryInterface(ABC):

    @abstractmethod
    def add():
        pass

    @abstractmethod
    def list():
        pass

    @abstractmethod
    def getById(id: str):
        pass

    @abstractmethod
    def getByname(name: str):
        pass

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def upsert():
        pass

    @abstractmethod
    def delete():
        pass