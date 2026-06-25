<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyMuPDF-FF6F00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" />
  <img src="https://img.shields.io/badge/DEEP--TRANSLATOR-00A86B?style=for-the-badge&logo=googletranslate&logoColor=white" />
  <img src="https://img.shields.io/badge/FPDF2-228B22?style=for-the-badge&logo=pdf&logoColor=white" />
  <img src="https://img.shields.io/badge/TKINTER-4B275F?style=for-the-badge&logo=python&logoColor=white" />
</p>

<h2 align="center">✨ Automated PDF Manual Translator & Layout Preserver ✨</h2>

<p align="center">
  Script utilitário e modular desenvolvido meticulosamente para automação de leitura, extração e tradução de manuais técnicos e documentos em PDF do inglês para o português (PT-BR). A plataforma dispõe de uma interface gráfica nativa (Tkinter) para seleção dinâmica de arquivos, processamento de texto página por página via PyMuPDF e tradução resiliente através da engine do deep-translator. O motor de saída reconstrói o arquivo em um novo PDF via fpdf2, injetando fontes TrueType (.ttf) localmente de forma totalmente automatizada para garantir a perfeita renderização e integridade de caracteres acentuados.
</p>

---

## 🎯 Objetivo do Projeto

O principal objetivo desta ferramenta é **quebrar a barreira do idioma em documentações técnicas**. 

Muitos equipamentos, sistemas e componentes possuem manuais densos e detalhados disponíveis exclusivamente em inglês. Este script foi criado para democratizar o acesso a essas informações essenciais, permitindo que qualquer usuário extraia, traduza e gere um novo documento em português de forma 100% automatizada. O foco é manter a organização e a paginação do material original, proporcionando uma leitura fluida, rápida e sem a necessidade de copiar e colar textos manualmente no Google Tradutor.

---

## ✨ Funcionalidades

* **Interface Amigável:** Utiliza o `tkinter` nativo para abrir caixas de diálogo do sistema operacional, eliminando a necessidade de digitar caminhos de pastas no terminal.
* **Tradução Automática:** Processamento e segmentação de texto por página, garantindo o respeito à paginação original do manual.
* **Suporte à Acentuação Nativa:** Carregamento dinâmico da fonte Arial TrueType para evitar falhas de codificação em caracteres como `á`, `ã`, `ç`.
* **Mapeamento de Destino Inteligente:** Identifica a pasta de origem do arquivo selecionado e gera o arquivo traduzido no mesmo diretório com o sufixo `_traduzido`.

---


## 📂 Estrutura do Projeto

```Bash
PDF-TRANSLATOR-PTBR/
├── fonts/
│   └── arial.ttf          # Fonte física para suporte a acentuação
├── venv/                  # Ambiente virtual integrado (ignorado)
├── .gitignore
├── LICENSE
├── main.py                # Script modular principal
├── README.md              # Documentação técnica do projeto
└── requirements.txt       # Manifesto de dependências do ecossistema
```

---

## 🧠 Arquitetura do Sistema

Abaixo está o fluxo detalhado de como o script processa o documento desde a seleção até a exportação final:

```mermaid
flowchart TD
    %% Nós de Início e Fim (Formato arredondado)
    Inicio(((INÍCIO DA EXECUÇÃO)))
    Fim_Erro(((FIM: Programa Encerrado)))
    Fim_Sucesso(((FIM DA EXECUÇÃO)))

    %% Passos do Processo (Formato retangular)
    Interface[INTERFACE GRÁFICA Tkinter<br>Abre a caixa de diálogo do sistema]
    Decisao{Usuário<br>selecionou<br>arquivo?}
    Arquivo_OK[ARQUIVO SELECIONADO<br>Ex: manual.pdf]
    Prep_Ambiente[PREPARAÇÃO DO AMBIENTE os.path<br>Cria a rota de saída ex: manual_traduzido.pdf]
    Motores[INICIALIZAÇÃO DOS MOTORES<br>1. GoogleTranslator<br>2. PyMuPDF fitz<br>3. fpdf2 com Arial.ttf]
    Exportacao[EXPORTAÇÃO FINAL<br>fpdf2 compila as páginas e salva o arquivo]

    %% Conexões principais
    Inicio --> Interface
    Interface --> Decisao
    
    %% Ramificações (Sim ou Não)
    Decisao -- Cancelou --> Fim_Erro
    Decisao -- Sim --> Arquivo_OK
    
    Arquivo_OK --> Prep_Ambiente
    Prep_Ambiente --> Motores
    
    %% O bloco do Loop (Agrupamento)
    Motores --> Loop
    
    subgraph Loop [LOOP DE PROCESSAMENTO - Para cada página]
        direction TB
        Extracao[1. EXTRAÇÃO: Lê todo o texto da página original]
        Traducao[2. TRADUÇÃO: Envia para Google Translate e recebe PT-BR]
        Escrita[3. ESCRITA: Cria nova página no PDF de saída,<br>imprime cabeçalho, e insere texto traduzido]
        
        Extracao --> Traducao --> Escrita
    end

    Loop --> Exportacao
    Exportacao --> Fim_Sucesso

    %% Estilos de cores (opcional para deixar mais profissional)
    style Inicio fill:#e6ffe6,stroke:#006600,stroke-width:2px
    style Fim_Erro fill:#ffe6e6,stroke:#990000,stroke-width:2px
    style Fim_Sucesso fill:#ffe6e6,stroke:#990000,stroke-width:2px
    style Decisao fill:#fff0b3,stroke:#b38600,stroke-width:2px
    style Loop fill:#f0f8ff,stroke:#005ce6,stroke-width:2px,stroke-dasharray: 5 5
```

## 🚀 Como Instalar e Rodar

1. Pré-requisitos
   Python 3.8 ou superior instalado.

Arquivo de fonte arial.ttf alocado dentro do diretório fonts/.

## 2. Configurando o Ambiente
```Bash
# Clonar o repositório
git clone [https://github.com/SEU-USUARIO/pdf-translator-ptbr.git](https://github.com/SEU-USUARIO/pdf-translator-ptbr.git)
cd pdf-translator-ptbr

# Inicializar e ativar o ambiente virtual (Windows)
python -m venv venv
venv\Scripts\activate

# Instalar as dependências do ecossistema
pip install -r requirements.txt
```

## 3. Execução
```Bash
python main.py
```

## 📄 Licença
Este projeto é distribuído sob os termos da licença incluída no arquivo LICENSE.