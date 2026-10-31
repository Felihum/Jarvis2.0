from flask import Flask
from views.collection_view import bp_collection
from views.pdf_view import bp_pdf
from src.modules.conversation import create_bp_conversation, ConversationService, OpenAIGateway, AnalyseIntentionUseCase, DefaultInteractionUseCase, SearchInteractionUseCase
from src.infrastructure.persistence import ChromadbAdapter
from services.bert_service import BertService
from src.utils.embedding import EmbeddingUtil
from chromadb import PersistentClient
import time

start_time = time.time()

print("[DEBUG] Iniciando a aplicação Flask...")
app = Flask(__name__)
print(f"[DEBUG] app Flask iniciado em: {time.time() - start_time:.4f} segundos")

embedding_util = EmbeddingUtil()

# DATABASE
vector_repository = ChromadbAdapter(chroma_client=PersistentClient("./db_data"), collection_name="chunks")

bert_service = BertService(embedding=embedding_util, vector_repository=vector_repository)

# GATEWAYS
conversation_gateway = OpenAIGateway()

# USE CASES
default_interaction_use_case = DefaultInteractionUseCase(conversation_gateway=conversation_gateway)
analyse_intention_use_case = AnalyseIntentionUseCase(conversation_gateway=conversation_gateway)
search_interaction_use_case = SearchInteractionUseCase(conversation_gateway=conversation_gateway, bert_service=bert_service)

# SERVICES
conversation_service = ConversationService( 
    analyse_intention=analyse_intention_use_case,
    interaction_use_cases=[
        default_interaction_use_case,
        search_interaction_use_case
    ]
)

# BLUEPRINTS
bp_conversation = create_bp_conversation(conversation_service=conversation_service)

# BLUEPRINTS REGISTRATION
app.register_blueprint(bp_collection)
app.register_blueprint(bp_pdf)
app.register_blueprint(bp_conversation)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, use_reloader=False)