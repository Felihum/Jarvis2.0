from abc import ABC, abstractmethod

class Service(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass