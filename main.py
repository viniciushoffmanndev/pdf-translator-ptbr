import os
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator

# ==========================================
# FUNÇÃO PRINCIPAL (SUBSTITUIÇÃO NO LOCAL)
# ==========================================

def processar_documento_in_place(caminho_entrada, caminho_saida):
    print(f"\nIniciando processo...\nA ler o ficheiro: {caminho_entrada}")
    
    # 1. Inicializa o tradutor
    tradutor = GoogleTranslator(source='en', target='pt')
    
    # 2. Abre o PDF original para edição
    doc = fitz.open(caminho_entrada)
    total_paginas = len(doc)
    
    for i in range(total_paginas):
        num_pagina = i + 1
        print(f"A processar página {num_pagina} de {total_paginas}...")
        
        pagina = doc.load_page(i)
        
        # Extrai os blocos da página
        blocos = pagina.get_text("blocks")
        
        for bloco in blocos:
            tipo_bloco = bloco[6]
            
            # Se for texto (0), nós processamos. Imagens (1) são ignoradas.
            if tipo_bloco == 0:
                texto_original = bloco[4].strip()
                
                if texto_original:
                    try:
                        # a) Traduz o texto
                        texto_traduzido = tradutor.translate(texto_original)
                        
                        # b) Higieniza o texto (Evita erros da fonte padrão do PDF)
                        # Remove aspas inteligentes e travessões longos
                        texto_traduzido = texto_traduzido.replace('“', '"').replace('”', '"')
                        texto_traduzido = texto_traduzido.replace('‘', "'").replace('’', "'")
                        texto_traduzido = texto_traduzido.replace('–', '-').replace('—', '-')
                        # Força o encoding para evitar travamento com emojis ou símbolos raros
                        texto_traduzido = texto_traduzido.encode('latin-1', 'ignore').decode('latin-1')
                        
                        # c) Captura as coordenadas originais
                        retangulo = fitz.Rect(bloco[:4])
                        
                        # d) Lógica de Fonte Dinâmica (Shrink-to-Fit)
                        # Descobre quantas linhas o texto original tinha para estimar a fonte
                        linhas_originais = max(1, len(texto_original.strip().split('\n')))
                        tamanho_fonte = min(12.0, (retangulo.height / linhas_originais) * 0.95)
                        
                        # Loop mágico: Tenta inserir o texto; se não couber, diminui a fonte e tenta de novo
                        while tamanho_fonte >= 4.0:
                            
                            # 1. Pinta o fundo de branco 
                            # (Isso também serve para apagar as tentativas que não couberam no loop anterior)
                            pagina.draw_rect(retangulo, color=(1, 1, 1), fill=(1, 1, 1))
                            
                            # 2. Tenta inserir o texto traduzido
                            rc = pagina.insert_textbox(
                                retangulo, 
                                texto_traduzido, 
                                fontsize=tamanho_fonte, 
                                fontname="helv", 
                                color=(0, 0, 0),
                                align=0
                            )
                            
                            # O 'rc' retorna o espaço restante. 
                            # Se for >= 0, significa que o texto coube perfeitamente sem ser cortado!
                            if rc >= 0:
                                break  # Encerra o loop, o tamanho está perfeito!
                                
                            # Se o 'rc' for negativo, o texto foi cortado. Diminuímos a fonte e tentamos de novo.
                            tamanho_fonte -= 0.5
                            
                    except Exception as e:
                        print(f"Erro ao processar um bloco na página {num_pagina}: {e}")
                        
    # 3. Guarda as alterações num novo ficheiro PDF
    doc.save(caminho_saida)
    doc.close()
    print(f"\nSucesso! Ficheiro traduzido e formatado guardado em: {caminho_saida}")

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
        
        processar_documento_in_place(ARQUIVO_ENTRADA, ARQUIVO_SAIDA)