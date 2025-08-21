import os
from dotenv import load_dotenv

from src.auth.google_auth import get_google_client
from src.services.sheet_service import SheetService
from src.services.api_service import ApiService

def main():

    NOME_DA_ABA_ALVO = "Base API Emendas Esp"

    try:
        # --- ETAPA 1: AUTENTICAÇÃO E CONFIGURAÇÃO ---
        print("1. Carregando configurações e autenticando...")
        load_dotenv()
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError("A variável de ambiente GOOGLE_APPLICATION_CREDENTIALS não foi definida")
        client = get_google_client(credentials_path)
        print("✓ Autenticação bem-sucedida!")

        # --- ETAPA 2: INICIALIZAR OS SERVIÇOS ---
        sheet_service = SheetService(client)
        api_service = ApiService()

        # --- ETAPA 3: BUSCAR DADOS DA API ---
        print("\n2. Buscando e processando dados da API externa...")
        dados_finais_df = api_service.fetch_and_process_data()

        # --- ETAPA 4: SALVAR DADOS NA PLANILHA ---
        print(f"\n3. Preparando para salvar relatório na aba '{NOME_DA_ABA_ALVO}'...")
        nome_planilha = 'planos_trabalho_completo_PE'

        spreadsheet = sheet_service.get_spreadsheet(nome_planilha)
        print(f"✓ Planilha '{spreadsheet.title}' encontrada!")

        sheet_service.update_worksheet_with_dataframe(spreadsheet, NOME_DA_ABA_ALVO, dados_finais_df)
        
        print("\nPROCESSO CONCLUÍDO COM SUCESSO!")

    except Exception as e:
        print(f"\n❌ ERRO NO PROCESSO: {str(e)}")

if __name__ == "__main__":
    main()