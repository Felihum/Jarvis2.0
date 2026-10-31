from flask import Blueprint, jsonify, request, Response, stream_with_context
from services.llm_service import LLMService
from config import DEFAULT_NPC

bp_llm = Blueprint("chatbot", __name__, url_prefix="/chatbot")

llm_service = LLMService()

#@bp_llm.route("/message", methods=["POST"])
#def message():
    #response = bert_service.search_query()

    #return jsonify({
        #"message": "Search results.",
        #"response": response
    #}), 200 

@bp_llm.route("/chat", methods=["POST"])
def chat():
    data = request.json

    npc_id = DEFAULT_NPC
    messages = data

    if isinstance(data, dict):
        npc_id = data.get("npc_id", DEFAULT_NPC)
        messages = data.get("messages", [])

    return Response(
        stream_with_context(llm_service.query(user_query=messages, npc_id=npc_id)),
        mimetype="text/event-stream"
    )

@bp_llm.route("/deep/<filename>", methods=["POST"])
def deep_analysing(filename: str):
    data = request.json
    return Response(stream_with_context(llm_service.deep_analysing(filename=filename, context=data)), mimetype='text/event-stream')