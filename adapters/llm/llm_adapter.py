from abc import ABC, abstractmethod
from typing import Iterator, Optional

class LLMAdapter(ABC):

    @abstractmethod
    def stream_chat(
        self,
        messages: list[dict],
        model: str
    ) -> Iterator[str]:
        """
        Deve retornar um iterator contendo apenas os tokens gerados pelo modelo.
        """
        pass

    @abstractmethod
    def single_response(
        self,
        message: list[dict],
        system: Optional[str],
        model: str,
        format: Optional[dict]
    ):
        pass