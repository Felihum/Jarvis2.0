from scripts.extract_pdf_content import processar_pdf, dividir_pdf
import chromadb
from sentence_transformers import SentenceTransformer
from flask import jsonify

PASTA_PDFS = "pdfs"
COLECAO_DISSERTACAO = "dissertacoes"
COLECAO_CHUNKS = "chunks"

class CollectionService:

    def insert_data(self, file, id_dissertation: int, title: str):

        print("🔍 Iniciando extração e limpeza dos PDFs...")
        dado = processar_pdf(file)

        print("🔍 Carregando modelo de embeddings (SentenceTransformer)...")
        modelo = SentenceTransformer("all-mpnet-base-v2")

        print("💾 Inicializando base vetorial (ChromaDB)...")
        client = chromadb.PersistentClient("./db_data")
        dissertation_collection = client.get_collection(name=COLECAO_DISSERTACAO)
        chunks_collection = client.get_collection(name=COLECAO_CHUNKS)

        embedding = modelo.encode(dado).tolist()

        context_chunks = dividir_pdf(file)
        chunk_embeddings = [modelo.encode(chunk).tolist() for chunk in context_chunks]

        dissertation_collection.add(
            ids=[str(id_dissertation)],
            documents=[dado],
            embeddings=[embedding],
            metadatas=[{
                "filename": file.filename,
                "title": title
            }],
        )

        chunk_ids = [f"{id_dissertation}_chunk_{i}" for i in range(len(context_chunks))]

        for i in range(len(chunk_embeddings)):
            print("Page Num: ", i+1)
            chunks_collection.add(
                ids=chunk_ids[i],
                documents=[context_chunks[i]],
                embeddings=[chunk_embeddings[i]],
                metadatas=[{
                    "filename": file.filename,
                    "page": i+1,
                    "title": title
                }]
            )

        print(f"\n✅ Dado inserido com sucesso!")
        return jsonify({
            "message": "Dado inserido com sucesso!"
        }), 200
