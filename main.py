
import os
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
from fpdf import FPDF

# ==========================================
# FUNÇÕES MODULARES
# ==========================================

def configurar_pdf_saida():
    """Cria o objeto FPDF, configura margens e carrega a fonte da pasta fonts."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    try:
        # Carrega a fonte Arial apontando para a pasta 'fonts'
        pdf.add_font('Arial', '', 'fonts/arial.ttf')
        pdf.set_font('Arial', size=11)
        print("Fonte Arial carregada com sucesso!")
    except Exception as e:
        # Se não achar o arquivo na pasta, não "quebra" o código, usa o padrão.
        print(f"Aviso: 'fonts/arial.ttf' não encontrado. Usando fonte padrão. ({e})")
        pdf.set_font("Helvetica", size=11)
        
    return pdf

def traduzir_texto(texto, tradutor):
    """Recebe um texto e retorna a versão traduzida."""
    if not texto.strip():
        return "[Página vazia ou sem texto extraível - provável imagem]."
    
    try:
        return tradutor.translate(texto)
    except Exception as e:
        print(f"Erro na tradução: {e}")
        return "[Erro ao traduzir o conteúdo desta página.]"

# ==========================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==========================================

def processar_documento(caminho_entrada, caminho_saida):
    """Coordena a leitura, tradução e criação do novo PDF."""
    print(f"Iniciando processo...\nLendo: {caminho_entrada}")
    
    # 1. Inicializa serviços e configurações
    tradutor = GoogleTranslator(source='en', target='pt')
    doc_original = fitz.open(caminho_entrada)
    pdf_saida = configurar_pdf_saida()
    
    total_paginas = len(doc_original)
    
    # 2. Loop de processamento de cada página
    for i in range(total_paginas):
        num_pagina = i + 1
        print(f"Processando página {num_pagina} de {total_paginas}...")
        
        # Extrai o texto
        pagina = doc_original.load_page(i)
        texto_original = pagina.get_text()
        
        # Traduz o texto
        texto_traduzido = traduzir_texto(texto_original, tradutor)
        
        # 3. Escreve no novo PDF
        pdf_saida.add_page()
        
        # Salva qual era a fonte base (Arial ou Helvetica configurada no início)
        fonte_base = pdf_saida.font_family
        
        # Cabeçalho da página (Sempre em Helvetica Negrito para não precisar do arquivo arialbd.ttf)
        pdf_saida.set_font("Helvetica", style="B", size=14)
        pdf_saida.cell(0, 10, text=f"PÁGINA {num_pagina}")
        pdf_saida.ln(10)
        
        # Retorna EXATAMENTE para a fonte base antes de imprimir o texto traduzido
        pdf_saida.set_font(fonte_base, size=11)
        pdf_saida.multi_cell(0, 6, text=texto_traduzido)
        
    # 4. Salva o resultado final
    pdf_saida.output(caminho_saida)
    print(f"\nSucesso! Arquivo salvo em: {caminho_saida}")

# ==========================================
# EXECUÇÃO DO SCRIPT
# ==========================================
if __name__ == "__main__":
    # 1. Inicia o Tkinter, mas oculta a janela principal (queremos só a caixa de diálogo)
    root = tk.Tk()
    root.withdraw()
    
    print("Aguardando seleção do arquivo...")
    
    # 2. Abre a janela para o usuário escolher o PDF
    ARQUIVO_ENTRADA = filedialog.askopenfilename(
        title="Selecione o PDF que deseja traduzir",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    
    # 3. Verifica se o usuário selecionou algo ou se clicou em "Cancelar"
    if not ARQUIVO_ENTRADA:
        print("❌ Nenhum arquivo foi selecionado. Encerrando o programa.")
    else:
        # 4. Cria o nome do arquivo de saída automaticamente na mesma pasta do original
        diretorio_origem = os.path.dirname(ARQUIVO_ENTRADA)
        nome_arquivo_original = os.path.basename(ARQUIVO_ENTRADA)
        
        # Pega o nome do arquivo sem a extensão ".pdf"
        nome_sem_extensao = os.path.splitext(nome_arquivo_original)[0]
        
        # Monta o caminho final de saída (ex: manual_traduzido.pdf)
        nome_arquivo_saida = f"{nome_sem_extensao}_traduzido.pdf"
        ARQUIVO_SAIDA = os.path.join(diretorio_origem, nome_arquivo_saida)
        
        print(f"\n📄 Arquivo selecionado: {ARQUIVO_ENTRADA}")
        print(f"💾 O PDF traduzido será salvo como: {ARQUIVO_SAIDA}\n")
        
        # 5. Roda a nossa função principal
        processar_documento(ARQUIVO_ENTRADA, ARQUIVO_SAIDA)