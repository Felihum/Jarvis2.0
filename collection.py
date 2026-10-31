# import chromadb

# COLECAO_DISSERTACAO = "dissertacoes"
# COLECAO_CHUNKS = "chunks"

# print("[DB] Inicializando base vetorial (ChromaDB)...")
# client = chromadb.PersistentClient("./db_data")
# dissertation_collection = client.get_or_create_collection(name=COLECAO_DISSERTACAO)
# chunks_collection = client.get_or_create_collection(name=COLECAO_CHUNKS)

import time
import chromadb

# Medição do tempo total de inicialização do ChromaDB
start_total = time.time()

COLECAO_DISSERTACAO = "dissertacoes"
COLECAO_CHUNKS = "chunks"

print("[DEBUG] [DB] Inicializando base vetorial (ChromaDB)...")

print("[DEBUG] Conectando ao PersistentClient (caminho: ./db_data)...")
start_time = time.time()
client = chromadb.PersistentClient("./db_data")
print(f"[DEBUG] -> PersistentClient inicializado com sucesso em {time.time() - start_time:.4f} segundos.")

print(f"[DEBUG] Obtendo ou criando coleção '{COLECAO_DISSERTACAO}'...")
start_time = time.time()
dissertation_collection = client.get_or_create_collection(name=COLECAO_DISSERTACAO)
print(f"[DEBUG] -> Coleção '{COLECAO_DISSERTACAO}' obtida/criada em {time.time() - start_time:.4f} segundos.")

print(f"[DEBUG] Obtendo ou criando coleção '{COLECAO_CHUNKS}'...")
start_time = time.time()
chunks_collection = client.get_or_create_collection(name=COLECAO_CHUNKS)
print(f"[DEBUG] -> Coleção '{COLECAO_CHUNKS}' obtida/criada em {time.time() - start_time:.4f} segundos.")

print(f"[DEBUG] Base vetorial (ChromaDB) totalmente inicializada em {time.time() - start_total:.4f} segundos no total.\n")