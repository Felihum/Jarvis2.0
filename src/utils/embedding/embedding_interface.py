from abc import ABC, abstractmethod

class EmbeddingInterface(ABC):

    @abstractmethod
    def encode(self, texts: list[str]):
        pass