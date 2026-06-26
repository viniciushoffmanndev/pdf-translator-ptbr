import os
import time  # <-- NOVO: Biblioteca para controlar o tempo e criar pausas
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import fitz
from deep_translator import GoogleTranslator

# ==========================================
# FUNÇÃO PRINCIPAL (SUBSTITUIÇÃO NO LOCAL)
# ==========================================

def processar_documento_in_place(caminho_entrada, caminho_saida, root):
    print(f"\nIniciando processo...\nA ler o ficheiro: {caminho_entrada}")
    
    # 1. Inicializa o tradutor e abre o PDF
    tradutor = GoogleTranslator(source='en', target='pt')
    doc = fitz.open(caminho_entrada)
    total_paginas = len(doc)
    
    # --- CRIANDO A JANELA DE PROGRESSO ---
    janela_progresso = tk.Toplevel(root)
    janela_progresso.title("Traduzindo PDF")
    janela_progresso.geometry("350x120")
    
    label_status = tk.Label(janela_progresso, text="A preparar documento...", font=("Arial", 10))
    label_status.pack(pady=15)
    
    barra_progresso = ttk.Progressbar(janela_progresso, orient="horizontal", length=280, mode="determinate")
    barra_progresso.pack(pady=5)
    barra_progresso["maximum"] = total_paginas
    # ----------------------------------------
    
    for i in range(total_paginas):
        num_pagina = i + 1
        
        # Atualiza a Interface Gráfica
        label_status.config(text=f"A traduzir página {num_pagina} de {total_paginas}...")
        barra_progresso["value"] = num_pagina
        janela_progresso.update() 
        
        print(f"A processar página {num_pagina} de {total_paginas}...")
        
        pagina = doc.load_page(i)
        blocos = pagina.get_text("blocks")
        
        for bloco in blocos:
            tipo_bloco = bloco[6]
            
            if tipo_bloco == 0:
                texto_original = bloco[4].strip()
                
                if texto_original:
                    try:
                        # a) Traduz o texto com Sistema de RESILIÊNCIA (Retry)
                        texto_traduzido = None
                        max_tentativas = 3
                        
                        for tentativa in range(max_tentativas):
                            try:
                                texto_traduzido = tradutor.translate(texto_original)
                                if texto_traduzido:
                                    break  # Traduziu com sucesso! Sai do laço de tentativas.
                                else:
                                    time.sleep(1.5)  # Veio vazio? Espera 1.5s e tenta de novo.
                            except Exception as erro_traducao:
                                print(f"Aviso de bloqueio na página {num_pagina}. Aguardando 3 segundos... (Tentativa {tentativa+1}/3)")
                                time.sleep(3)  # Erro de conexão/Google? Pausa 3s para o servidor "acalmar".
                                
                        # Se depois das 3 tentativas ainda estiver vazio, aí sim ele pula.
                        if not texto_traduzido:
                            continue
                            
                        # b) Higieniza o texto
                        texto_traduzido = texto_traduzido.replace('“', '"').replace('”', '"')
                        texto_traduzido = texto_traduzido.replace('‘', "'").replace('’', "'")
                        texto_traduzido = texto_traduzido.replace('–', '-').replace('—', '-')
                        texto_traduzido = texto_traduzido.encode('latin-1', 'ignore').decode('latin-1')
                        
                        # c) Captura as coordenadas originais
                        retangulo = fitz.Rect(bloco[:4])
                        
                        # d) Lógica de Fonte Dinâmica (Shrink-to-Fit)
                        linhas_originais = max(1, len(texto_original.strip().split('\n')))
                        tamanho_fonte = min(12.0, (retangulo.height / linhas_originais) * 0.95)
                        
                        while tamanho_fonte >= 4.0:
                            pagina.draw_rect(retangulo, color=(1, 1, 1), fill=(1, 1, 1))
                            rc = pagina.insert_textbox(
                                retangulo, 
                                texto_traduzido, 
                                fontsize=tamanho_fonte, 
                                fontname="helv", 
                                color=(0, 0, 0),
                                align=0
                            )
                            if rc >= 0:
                                break
                            tamanho_fonte -= 0.5
                            
                    except Exception as e:
                        print(f"Erro gráfico ao processar um bloco na página {num_pagina}: {e}")
                        
        # Adiciona um freio extra a cada página finalizada para segurança
        time.sleep(0.5)
                        
    # 3. Guarda as alterações num novo ficheiro PDF
    label_status.config(text="Concluído! A guardar ficheiro...")
    janela_progresso.update()
    
    doc.save(caminho_saida)
    doc.close()
    
    janela_progresso.destroy() 
    print(f"\nSucesso! Ficheiro traduzido e formatado guardado em: {caminho_saida}")

    messagebox.showinfo(
        title="Tradução Concluída",
        message=f"O PDF foi traduzido com sucesso e o layout original foi mantido!\n\nArquivo salvo em:\n{caminho_saida}"
    )

# ==========================================
# EXECUÇÃO DO SCRIPT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    print("A aguardar seleção do ficheiro...")
    
    ARQUIVO_ENTRADA = filedialog.askopenfilename(
        title="Selecione o PDF que deseja traduzir",
        filetypes=[("Ficheiros PDF", "*.pdf")]
    )
    
    if not ARQUIVO_ENTRADA:
        print("Nenhum ficheiro foi selecionado. A encerrar o programa.")
    else:
        diretorio_origem = os.path.dirname(ARQUIVO_ENTRADA)
        nome_arquivo_original = os.path.basename(ARQUIVO_ENTRADA)
        nome_sem_extensao = os.path.splitext(nome_arquivo_original)[0]
        
        nome_arquivo_saida = f"{nome_sem_extensao}_layout_mantido.pdf"
        ARQUIVO_SAIDA = os.path.join(diretorio_origem, nome_arquivo_saida)
        
        processar_documento_in_place(ARQUIVO_ENTRADA, ARQUIVO_SAIDA, root)