from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Document:
    id: str
    content: str
    metadata: Dict[str, any] = field(default_factory=dict)
    vector: Optional[List[float]] = (
        None
    )

@dataclass
class SearchQuery:
    vector: List[float]
    top_k: int = 5
    filter: Optional[Dict[str, any]] = (
        None
    )

@dataclass
class SearchResult:
    document: Document
    score: float

class VectorDatabaseInterface(ABC):
    @abstractmethod
    def save(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    def search(self, query: SearchQuery) -> List[SearchResult]:
        pass

    @abstractmethod
    def delete(self, document_ids: List[str]) -> None:
        pass