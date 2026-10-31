import re
import PyPDF2
from tqdm import tqdm  # apenas para barra de progresso

# Caminho da pasta com os PDFs
PASTA_PDFS = "pdfs"
ARQUIVO_SAIDA = "dissertacoes_limpos.json"

# --- Função para extrair texto de um PDF ---
def extrair_texto_pdf(pdf):
    try:
        leitor = PyPDF2.PdfReader(pdf)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto
    except Exception as e:
        print(f"Erro ao ler {pdf}: {e}")
        return ""

# --- Função para limpar o texto ---
def limpar_texto(texto):
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)       # remove espaços extras
    texto = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ0-9.,;:?!()\"'%\s-]", "", texto)
    # texto = texto.lower()  # remove símbolos estranhos
    return texto.strip()

# --- Função para dividir o texto em chunks menores ---
# def dividir_texto(texto, max_palavras=1000):
#     palavras = texto.split(" ")
#     chunks = []
#     for i in range(0, len(palavras), max_palavras):
#         trecho = " ".join(palavras[i:i+max_palavras]).strip()
#         if len(trecho) > 100:  # evita blocos muito pequenos
#             chunks.append(trecho)
#     return chunks

def dividir_pdf(pdf):
    try:
        leitor = PyPDF2.PdfReader(pdf)
        paginas = [pagina.extract_text() or "" for pagina in leitor.pages]
        return paginas
    except Exception as e:
        print(f"Erro ao ler {pdf}: {e}")
        return ""

def processar_pdf(pdf):
    texto = extrair_texto_pdf(pdf)
    texto_limpo = limpar_texto(texto)

    return texto_limpo
