# gui/main_window.py
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import subprocess

textos_extraidos = []


def iniciar_app():
    global entrada_termo, caixa_resultado

    root = tk.Tk()
    root.title("Leitor de Diários Oficiais")
    root.geometry("800x600")

    label = tk.Label(root, text="Selecione os arquivos PDF:")
    label.pack(pady=10)

    btn_selecionar = tk.Button(root, text="Selecionar PDFs", command=selecionar_pdfs)
    btn_selecionar.pack(pady=5)

    label_busca = tk.Label(root, text="Buscar termo:")
    label_busca.pack(pady=10)

    entrada_termo = tk.Entry(root, width=50)
    entrada_termo.pack(pady=5)

    btn_buscar = tk.Button(root, text="Buscar", command=buscar_termo)
    btn_buscar.pack(pady=5)

    caixa_resultado = scrolledtext.ScrolledText(root, width=90, height=20)
    caixa_resultado.pack(pady=10)

    btn_abrir_resultado = tk.Button(root, text="Abrir arquivo de resultados", command=abrir_arquivo_resultado)
    btn_abrir_resultado.pack(pady=5)

    btn_gerar_pergunta = tk.Button(root, text="Gerar Pergunta IA", command=gerar_pergunta_ia)
    btn_gerar_pergunta.pack(pady=5)

    root.mainloop()


def selecionar_pdfs():
    global textos_extraidos
    arquivos = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if arquivos:
        from core.pdf_reader import extrair_texto_de_pdfs
        textos_extraidos = extrair_texto_de_pdfs(arquivos)
        messagebox.showinfo("Sucesso", f"{len(textos_extraidos)} arquivos processados com sucesso.")


def buscar_termo():
    from core.search_engine import buscar_termo_em_textos
    termo = entrada_termo.get()
    if not termo:
        messagebox.showwarning("Aviso", "Digite um termo para buscar.")
        return

    resultados = buscar_termo_em_textos(termo, textos_extraidos)
    caixa_resultado.delete('1.0', tk.END)
    if resultados:
        from core.file_manager import salvar_resultados
        salvar_resultados(resultados, "data/resultados.txt")
        for r in resultados:
            caixa_resultado.insert(tk.END, r + "\n\n")
    else:
        caixa_resultado.insert(tk.END, "Nenhuma ocorrência encontrada.")


def abrir_arquivo_resultado():
    caminho = os.path.abspath("data/resultados.txt")
    if os.path.exists(caminho):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(caminho)
            elif os.name == 'posix':  # macOS / Linux
                subprocess.call(('xdg-open', caminho))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")
    else:
        messagebox.showinfo("Arquivo não encontrado", "Nenhum resultado salvo foi encontrado ainda.")


def gerar_pergunta_ia():
    from core.question_generator import gerar_pergunta
    texto = caixa_resultado.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Nenhuma decisão para gerar pergunta.")
        return
    pergunta = gerar_pergunta(texto)
    caixa_resultado.insert(tk.END, f"\n\nSugestão de Pergunta IA: {pergunta}\n")