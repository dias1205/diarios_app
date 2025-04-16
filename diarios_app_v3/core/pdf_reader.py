# core/pdf_reader.py
import fitz  # PyMuPDF

def extrair_texto_de_pdfs(caminhos):
    textos = []
    for caminho in caminhos:
        try:
            doc = fitz.open(caminho)
            texto_total = ""
            for pagina in doc:
                texto_total += pagina.get_text()
            textos.append(texto_total)
        except Exception as e:
            textos.append(f"Erro ao ler {caminho}: {str(e)}")
    return textos