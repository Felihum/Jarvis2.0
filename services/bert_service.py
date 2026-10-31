# from collection import dissertation_collection, chunks_collection
from src.utils.embedding import EmbeddingInterface
from src.infrastructure.persistence import VectorDatabaseInterface, SearchQuery
from typing import Optional


class BertService:

    def __init__(
        self, 
        embedding: EmbeddingInterface, 
        vector_repository: VectorDatabaseInterface
    ):
        self.embedding = embedding
        self.vector_repository = vector_repository

    def search_query_fast(
        self,
        query: Optional[str] = None,
        chunks_num: int = 4,
    ):
        if not query:
            return {
                "response": [],
                "context": [],
                "filenames": [],
                "titles": [],
                "best_distance": None
            }

        # 1. Gera o vetor da query utilizando o serviço de embedding
        vector_query = self.embedding.encode([query]).tolist()[0]

        # 2. Cria o Objeto de Valor de Domínio para a busca
        search_query = SearchQuery(
            vector=vector_query,
            top_k=chunks_num
        )

        # 3. Executa a busca através da Porta (Totalmente desacoplado do ChromaDB)
        search_results = self.vector_repository.search(search_query)

        response = []
        contexts = []
        filenames = set()
        titles = set()
        best_distance = None

        # 4. Processa os resultados padronizados vindos da porta
        for i, result in enumerate(search_results):
            document = result.document
            distance = result.score  # Nota: dependendo da sua implementação, o score pode ser distância ou similaridade

            if distance is not None:
                if best_distance is None or distance < best_distance:
                    best_distance = distance

            # Extrai metadados do documento de domínio
            filename = document.metadata.get("filename", "")
            title = document.metadata.get("title", filename)
            page = document.metadata.get("page")

            if filename:
                filenames.add(filename)

            if title:
                titles.add(title)

            item = {
                "filename": filename,
                "title": title,
                "page": page,
                "rank": i + 1,
                "distance": distance
            }

            response.append(item)

            contexts.append({
                "filename": filename,
                "title": title,
                "page": page,
                "chunk": document.content,
                "distance": distance
            })

        return {
            "response": response,
            "context": contexts,
            "filenames": list(filenames),
            "titles": list(titles),
            "best_distance": best_distance
        }

    # def search_query(
    #     self,
    #     query: Optional[str] = None,
    #     dissertations_num: int = 3,
    #     chunks_num: int = 6
    # ):
        
    #     if not query:
    #         return {
    #             "response": [],
    #             "context": []
    #         }

    #     embedding_query = EmbeddingService.encode([query]).tolist()

    #     dissertation_results = dissertation_collection.query(
    #         query_embeddings=embedding_query,
    #         n_results=dissertations_num
    #     )

    #     response = []
    #     contexts = []

    #     documents = dissertation_results.get("documents", [[]])[0]
    #     metadatas = dissertation_results.get("metadatas", [[]])[0]
    #     distances = dissertation_results.get("distances", [[]])[0]

    #     for i, content in enumerate(documents):
    #         metadata = metadatas[i]
    #         filename = metadata.get("filename", "")
    #         title = metadata.get("title", filename)
    #         distance = distances[i] if i < len(distances) else None

    #         response.append({
    #             "filename": filename,
    #             "title": title,
    #             "resume": content[:1500],
    #             "rank": i + 1,
    #             "distance": distance
    #         })

    #         chunk_result = chunks_collection.query(
    #             query_embeddings=embedding_query,
    #             n_results=chunks_num,
    #             where={
    #                 "filename": filename
    #             }
    #         )

    #         chunk_documents = chunk_result.get("documents", [[]])[0]
    #         chunk_metadatas = chunk_result.get("metadatas", [[]])[0]
    #         chunk_distances = chunk_result.get("distances", [[]])[0]

    #         for j, chunk in enumerate(chunk_documents):
    #             chunk_metadata = chunk_metadatas[j] if j < len(chunk_metadatas) else {}
    #             chunk_distance = chunk_distances[j] if j < len(chunk_distances) else None

    #             contexts.append({
    #                 "filename": filename,
    #                 "title": title,
    #                 "page": chunk_metadata.get("page"),
    #                 "chunk": chunk,
    #                 "distance": chunk_distance
    #             })

    #     return {
    #         "response": response,
    #         "context": contexts
    #     }

    # def deep_search(self, filename: str):
    #     print("Iniciando deep search")
    #     chunks = chunks_collection.get(where={"filename": filename}, limit=30)
    #     print("Deep search finalizado")
    #     return chunks["documents"], chunks["metadatas"]
