from abc import ABC, abstractmethod
from typing import Iterator, Optional

class ConversationGateway(ABC):

    @abstractmethod
    def stream_chat(self, messages: list[dict]) -> Iterator[str]:
        pass

    @abstractmethod
    def single_response(self, message: list[dict], system: Optional[str], format: Optional[dict]):
        pass