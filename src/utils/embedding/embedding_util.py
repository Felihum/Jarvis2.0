
from sentence_transformers import SentenceTransformer
from .embedding_interface import EmbeddingInterface

class EmbeddingUtil(EmbeddingInterface):
    def __init__(self):
        print("Estabelecendo conexão com Hugging Face e carregando modelo de embeddings (SentenceTransformer)...")
        self.model = SentenceTransformer("all-mpnet-base-v2", device="cpu")

    def encode(self, texts: list[str]):
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )