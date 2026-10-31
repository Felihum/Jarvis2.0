from flask import jsonify, send_file
import os

PASTA_PDFS = os.path.join(os.getcwd(), "pdfs")

class PdfService:

    def get_pdf_by_name(self, filename: str):
        file_path = os.path.join(PASTA_PDFS, filename)

        print(f"🔍 Procurando arquivo PDF em: {file_path}")

        if not os.path.isfile(file_path):
            return jsonify({"erro": "Arquivo não encontrado."}), 404

        return send_file(file_path, mimetype="application/pdf")
