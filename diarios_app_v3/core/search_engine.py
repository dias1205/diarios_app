# core/search_engine.py
import re

def buscar_termo_em_textos(termo, textos):
    resultados = []
    for texto in textos:
        if termo.lower() in texto.lower():
            ementas = extrair_ementas(texto)
            resultados.extend(ementas)
    return resultados


def extrair_ementas(texto):
    padrao_ementa = re.compile(r'(?:Ementa:|Inteiro teor:).*?(?=(?:\n\s*Ementa:|\n\s*Inteiro teor:|$))', re.IGNORECASE | re.DOTALL)
    return [m.group().strip() for m in padrao_ementa.finditer(texto)]