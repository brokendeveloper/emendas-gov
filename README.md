# Projeto de Automação de Emendas Parlamentares

## 📖 Descrição

Este projeto automatiza a coleta, processamento e armazenamento de dados referentes a emendas parlamentares especiais do governo. A aplicação busca dados da API pública `transferegov.gestao.gov.br`, realiza o tratamento e a união das informações relevantes e, por fim, atualiza uma planilha no Google Sheets com o relatório final.

O objetivo é manter uma base de dados sempre atualizada para consulta e análise, eliminando a necessidade de extração manual.

## ✨ Funcionalidades Principais

- **Autenticação Segura:** Utiliza uma conta de serviço do Google Cloud para se autenticar de forma segura com a API do Google Sheets.
- **Coleta de Dados via API:** Busca informações de planos de ação, executores e planos de trabalho diretamente da fonte oficial.
- **Processamento e Limpeza:** Utiliza a biblioteca `pandas` para unir, filtrar e formatar os dados, gerando um relatório coeso.
- **Atualização Inteligente da Planilha:** Verifica se a aba de destino já existe na planilha. Se existir, ela é limpa antes de receber os novos dados. Caso contrário, uma nova aba é criada automaticamente.
- **Configuração Flexível:** O nome da planilha e o caminho para as credenciais são configuráveis através de variáveis no código e em um arquivo `.env`.

## 🚀 Como Utilizar

### Pré-requisitos

- **Python 3.8 ou superior**
- **Pip** (gerenciador de pacotes do Python)
- **Conta de Serviço do Google Cloud:** É necessário ter um arquivo de credenciais (`.json`) com permissão para acessar e editar a API do Google Sheets. [Siga este guia para criar uma](https://docs.gspread.org/en/latest/oauth2.html).
- **Compartilhar a Planilha:** A planilha do Google Sheets que você deseja atualizar deve ser compartilhada com o email do cliente (`client_email`) que está no seu arquivo de credenciais `.json`.

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd emendas-gov
```

### 2. Configurar o Ambiente

É altamente recomendado o uso de um ambiente virtual (`venv`) para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
# No Linux ou macOS:
source venv/bin/activate
# No Windows:
.\venv\Scripts\activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurar as Credenciais

1.  **Arquivo de Credenciais:** Coloque o arquivo `.json` da sua conta de serviço do Google dentro da pasta `config/credentials/`.
2.  **Arquivo de Ambiente (`.env`):** Crie um arquivo chamado `.env` na raiz do projeto. Dentro dele, adicione a seguinte linha, substituindo `seu-arquivo.json` pelo nome do seu arquivo de credencial:

    ```env
    GOOGLE_APPLICATION_CREDENTIALS="config/credentials/seu-arquivo.json"
    ```

### 5. Configurar o Script Principal

Abra o arquivo `main.py` e, se desejar, altere as variáveis no início da função `main()`:

- `NOME_DA_ABA_ALVO`: Nome da aba que será criada ou atualizada na sua planilha.
- `nome_planilha`: Nome exato da sua planilha no Google Sheets.

### 6. Executar o Projeto

Para iniciar o processo de automação, basta executar o script principal:

```bash
python main.py
```

O terminal exibirá o progresso, desde a autenticação até a conclusão do upload dos dados para a planilha. Em caso de erro, uma mensagem será exibida para ajudar a identificar o problema.
