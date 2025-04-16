# core/file_manager.py
import os
from fpdf import FPDF
import re

def salvar_resultados(resultados, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        for resultado in resultados:
            f.write(resultado + '\n\n')
    return True

def gerar_pdf_decisoes_filtradas(decisoes, filtros, pasta_saida="data/pdf_decisoes"):
    os.makedirs(pasta_saida, exist_ok=True)
    for texto in decisoes:
        if not atende_filtros(texto, filtros):
            continue
        numero_processo = extrair_numero_processo(texto)
        nome_arquivo = f"Ementa decisão nº {numero_processo}.pdf" if numero_processo else "decisao_sem_numero.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for linha in texto.split('\n'):
            pdf.multi_cell(0, 10, linha)
        pdf.output(os.path.join(pasta_saida, nome_arquivo))

def extrair_numero_processo(texto):
    match = re.search(r"\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{4}\.\d{1,2}", texto)
    if match:
        return match.group()
    return None

def atende_filtros(texto, filtros):
    comarca = filtros.get("comarca", "").lower()
    tribunal = filtros.get("tribunal", "").lower()
    area = filtros.get("area", "").lower()
    decisao_tipo = filtros.get("decisao", "").lower()
    numero_processo = filtros.get("numero_processo", "")

    return all([
        comarca in texto.lower() if comarca else True,
        tribunal in texto.lower() if tribunal else True,
        area in texto.lower() if area else True,
        decisao_tipo in texto.lower() if decisao_tipo else True,
        numero_processo in texto if numero_processo else True
    ])
