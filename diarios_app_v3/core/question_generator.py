import json
import os
from sentence_transformers import SentenceTransformer, util

modelo = SentenceTransformer('all-MiniLM-L6-v2')

def carregar_exemplos(caminho="data/exemplos.json"):
    if not os.path.exists(caminho):
        return [], []
    with open(caminho, 'r', encoding='utf-8') as f:
        exemplos = json.load(f)
    decisoes = [e['decisao'] for e in exemplos]
    perguntas = [e['pergunta'] for e in exemplos]
    vetores = modelo.encode(decisoes, convert_to_tensor=True)
    return vetores, perguntas

vetores_exemplo, perguntas_exemplo = carregar_exemplos()

def gerar_pergunta(texto):
    if not vetores_exemplo:
        return "Base de perguntas ainda não carregada ou vazia."
    vetor_texto = modelo.encode(texto, convert_to_tensor=True)
    similaridades = util.pytorch_cos_sim(vetor_texto, vetores_exemplo)
    idx = similaridades.argmax()
    return perguntas_exemplo[idx]
