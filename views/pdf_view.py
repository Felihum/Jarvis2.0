from flask import Blueprint, request
from services.pdf_service import PdfService

bp_pdf = Blueprint("pdf", __name__, url_prefix="/pdf")

pdf_service = PdfService()

@bp_pdf.route("/", methods=["GET"])
def get_pdf_by_name():
    filename = request.args.get("filename")

    if not filename:
        return {"erro": "Nenhum nome de arquivo fornecido"}, 400
    
    return pdf_service.get_pdf_by_name(filename=filename)