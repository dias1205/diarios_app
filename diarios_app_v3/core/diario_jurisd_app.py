# diario_jurisd_app.py
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from fpdf import FPDF

# Função para salvar os textos extraídos dos PDFs em um arquivo .txt
def salvar_resultados(resultados, caminho_saida):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        for resultado in resultados:
            f.write(resultado + '\n\n')
    return True

# Função para gerar PDFs filtrando decisões por critérios

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

# Regex para identificar número do processo

def extrair_numero_processo(texto):
    match = re.search(r"\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{4}\.\d{1,2}", texto)
    if match:
        return match.group()
    return None

# Verifica se o texto atende aos filtros informados

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

# Interface gráfica para seleção de filtros e geração dos PDFs

if __name__ == '__main__':
    def gerar_pdf():
        filtros = {
            "comarca": entry_comarca.get(),
            "tribunal": entry_tribunal.get(),
            "area": entry_area.get(),
            "decisao": entry_decisao.get(),
            "numero_processo": entry_numero.get(),
        }
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo de texto com decisões",
            filetypes=[("Text files", "*.txt")]
        )
        if not caminho:
            return
        with open(caminho, 'r', encoding='utf-8') as f:
            decisoes = f.read().split('\n\n')
        gerar_pdf_decisoes_filtradas(decisoes, filtros)
        messagebox.showinfo("Sucesso", "PDFs gerados com sucesso!")

    root = tk.Tk()
    root.title("Gerador de PDFs de Decisões")

    ttk.Label(root, text="Comarca:").grid(row=0, column=0, sticky='e')
    entry_comarca = ttk.Entry(root, width=40)
    entry_comarca.grid(row=0, column=1)

    ttk.Label(root, text="Tribunal:").grid(row=1, column=0, sticky='e')
    entry_tribunal = ttk.Entry(root, width=40)
    entry_tribunal.grid(row=1, column=1)

    ttk.Label(root, text="Área do Direito:").grid(row=2, column=0, sticky='e')
    entry_area = ttk.Entry(root, width=40)
    entry_area.grid(row=2, column=1)

    ttk.Label(root, text="Tipo de Decisão:").grid(row=3, column=0, sticky='e')
    entry_decisao = ttk.Entry(root, width=40)
    entry_decisao.grid(row=3, column=1)

    ttk.Label(root, text="Número do Processo:").grid(row=4, column=0, sticky='e')
    entry_numero = ttk.Entry(root, width=40)
    entry_numero.grid(row=4, column=1)

    ttk.Button(root, text="Gerar PDFs", command=gerar_pdf).grid(row=5, columnspan=2, pady=10)

    root.mainloop()
