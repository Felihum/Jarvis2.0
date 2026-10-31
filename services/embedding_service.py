from sentence_transformers import SentenceTransformer

try:
    import torch
except ImportError:
    torch = None


class EmbeddingService:
    _model = None
    _device = None

    @classmethod
    def get_device(cls):
        if cls._device is None:
            if torch is not None and torch.cuda.is_available():
                cls._device = "cuda"
            else:
                cls._device = "cpu"
        return cls._device

    @classmethod
    def get_model(cls):
        if cls._model is None:
            device = cls.get_device()
            print(f"Carregando modelo de embeddings em: {device}")
            cls._model = SentenceTransformer("all-mpnet-base-v2", device=device)
        return cls._model

    @classmethod
    def encode(cls, texts):
        model = cls.get_model()
        return model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )