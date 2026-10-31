import os
import json
from flask import request, Blueprint, jsonify
from services.collection_service import CollectionService

bp_collection = Blueprint("collection", __name__, url_prefix="/collection")

collection_service = CollectionService()

@bp_collection.route("/", methods=["POST"])
def insert_data():
    if 'dissertation_file' not in request.files:
        return {"erro": "Nenhum arquivo enviado"}, 400

    dissertation_file = request.files['dissertation_file']  # <--- aqui você recebe o arquivo
    id_dissertation = request.form.get("id_dissertation")
    title = request.form.get("title")

    return collection_service.insert_data(file=dissertation_file, id_dissertation=id_dissertation, title=title)

@bp_collection.route("/metadata", methods=["GET"])
def get_metadata():
    caminho_metadados = os.path.join(os.getcwd(), "metadados.json")
    if not os.path.exists(caminho_metadados):
        #retorna erro 404 caso o script de indexacao em lote ainda nao tenha sido executado
        return jsonify({"erro": "Arquivo metadados.json não encontrado. Execute a indexação primeiro."}), 404

    try:
        with open(caminho_metadados, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao ler os metadados: {str(e)}"}), 500