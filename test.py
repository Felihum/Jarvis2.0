from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def extrair_texto_por_pagina(caminho_pdf):
    textos = {}

    for numero_pagina, page in enumerate(extract_pages(caminho_pdf), start=1):
        texto_pagina = ""

        for element in page:
            if isinstance(element, LTTextContainer):
                texto_pagina += element.get_text()

        textos[numero_pagina] = texto_pagina.strip()

    return textos


# Exemplo de uso
texto_por_pagina = extrair_texto_por_pagina("./pdfs/dissertacao8.pdf")

for pagina, texto in texto_por_pagina.items():
    print(f"\n===== Página {pagina} =====\n")
    print(texto)
