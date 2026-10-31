from flask import Blueprint, json, request, abort, Response, stream_with_context
from config import DEFAULT_NPC
from dataclasses import dataclass, field
from src.modules.conversation.domain.models import ConversationMessage
from src.modules.shared import Service

@dataclass
class ChatRequestPayload:
    npc_id: str | None = DEFAULT_NPC
    messages: list[ConversationMessage] = field(default_factory=list)

def create_bp_conversation(conversation_service: Service):
    bp_conversation = Blueprint("chatbot", __name__, url_prefix="/chatbot")

    @bp_conversation.route("/chat", methods=["POST"])
    def chat():
        print(f"Received request with payload: {request.json}")
        try:
            payload = ChatRequestPayload(**request.json)
        except TypeError:
            abort(400, description="Payload com formato incorreto")

        def generate_chunks():
            for chunk in conversation_service.execute(user_query=payload.messages, npc_id=payload.npc_id):                
                yield f"data: {json.dumps(chunk.to_dict())}\n\n".encode('utf-8')

        return Response(
            stream_with_context(generate_chunks()),
            mimetype="text/event-stream"
        )
    
    return bp_conversation