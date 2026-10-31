from src.infrastructure.persistence.application.vector_database_interface import VectorDatabaseInterface, Document, SearchQuery, SearchResult
from chromadb.api import ClientAPI
from typing import List

class ChromadbAdapter(VectorDatabaseInterface):
    def __init__(self, chroma_client: ClientAPI, collection_name: str = "meu_projeto"):
        self.client = chroma_client
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def save(self, documents: List[Document]) -> None:
        ids = [doc.id for doc in documents]
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        vectors = [doc.vector for doc in documents if doc.vector is not None]

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=vectors if vectors else None,
        )

    def search(self, query: SearchQuery) -> List[SearchResult]:
        results = self.collection.query(
            query_embeddings=[query.vector],
            n_results=query.top_k,
            where=query.filter,
        )

        search_results = []
        
        if results and results.get("ids") and len(results["ids"]) > 0:
            ids = results["ids"][0]
            documents = results["documents"][0]
            
            metadatas = (
                results["metadatas"][0] 
                if results.get("metadatas") and len(results["metadatas"]) > 0 
                else [{}] * len(ids)
            )
            
            distances = (
                results["distances"][0] 
                if results.get("distances") and len(results["distances"]) > 0 
                else [0.0] * len(ids)
            )

            for i in range(len(ids)):
                doc = Document(
                    id=ids[i],
                    content=documents[i],
                    metadata=metadatas[i] if i < len(metadatas) and metadatas[i] else {},
                )
                
                distance = distances[i] if i < len(distances) else 0.0
                score = 1.0 - distance if distance <= 1.0 else 0.0

                search_results.append(SearchResult(document=doc, score=score))

        return search_results
    
    def delete(self, document_ids: List[str]) -> None:
        self.collection.delete(ids=document_ids)