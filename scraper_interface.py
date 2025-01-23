import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import pandas as pd

def coletar_livros(url, text_widget, resultados):
    try:
        # Fazendo a requisição para a página
        response = requests.get(url)
        response.raise_for_status()

        # Processando o conteúdo da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrando os livros
        livros = soup.find_all('article', class_='product_pod')

        if not livros:
            messagebox.showwarning("Aviso", "Não foi possível encontrar livros. Verifique a estrutura do site.")
            return

        text_widget.delete(1.0, tk.END)  # Limpar o campo de texto
        resultados.clear()  # Limpar resultados anteriores
        for livro in livros:
            # Capturar o título do livro
            titulo = livro.find('h3').a['title']

            # Capturar o preço do livro
            preco = livro.find('p', class_='price_color').get_text(strip=True)

            # Capturar a URL da imagem do livro
            imagem_tag = livro.find('img')
            imagem = imagem_tag['src'] if imagem_tag and 'src' in imagem_tag.attrs else "Imagem não encontrada"

            # Adicionar os resultados ao campo de texto
            text_widget.insert(tk.END, f"Título: {titulo}\nPreço: {preco}\nImagem: {imagem}\n\n")
            resultados.append({"Título": titulo, "Preço": preco, "Imagem": imagem})

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao acessar o site: {e}")

def salvar_para_excel(resultados):
    if not resultados:
        messagebox.showwarning("Aviso", "Nenhum dado para salvar. Execute o scraper primeiro.")
        return

    # Abrir diálogo para salvar o arquivo
    arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")], title="Salvar como")

    if not arquivo:
        return  # Cancelar salvar

    # Criar um DataFrame e salvar em Excel
    df = pd.DataFrame(resultados)
    df.to_excel(arquivo, index=False)
    messagebox.showinfo("Sucesso", f"Os dados foram salvos em {arquivo}!")

def criar_interface():
    # Criar a janela principal
    janela = tk.Tk()
    janela.title("Scraper de Livros")
    janela.geometry("700x500")  # Aumentar o tamanho da janela

    resultados = []  # Lista para armazenar os resultados

    # Rótulo
    label = tk.Label(janela, text="Clique no botão para coletar dados de livros", font=("Arial", 14))
    label.pack(pady=10)

    # Campo de texto para exibir os resultados
    text_widget = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=80, height=20, font=("Arial", 10))
    text_widget.pack(pady=10)

    # Botão para executar o scraper
    botao_coletar = tk.Button(janela, text="Coletar Livros", font=("Arial", 14), bg="lightblue", command=lambda: coletar_livros("http://books.toscrape.com/", text_widget, resultados))
    botao_coletar.pack(pady=10)

    # Botão para salvar os dados em Excel
    botao_salvar = tk.Button(janela, text="Salvar em Excel", font=("Arial", 14), bg="lightgreen", command=lambda: salvar_para_excel(resultados))
    botao_salvar.pack(pady=10)

    # Executar a interface
    janela.mainloop()

# Executar a interface gráfica
criar_interface()

