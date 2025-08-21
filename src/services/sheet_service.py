import gspread 
from gspread_dataframe import set_with_dataframe

class SheetService:
    def __init__(self, client):
        self.client = client

    def get_spreadsheet(self, spreadsheet_name):
        """Abre uma planilha pelo nome"""
        try:
            return self.client.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            raise Exception(f"ERRO: A planilha com o nome '{spreadsheet_name}' não foi encontrada. Verifique o nome ou as permissões de compartilhamento.")
        except Exception as e:
            raise Exception(f"Erro ao abrir planilha: {str(e)}")

    def list_worksheets(self, spreadsheet):
        """Lista todas as abas da planilha"""
        return [(idx, worksheet.title) for idx, worksheet in enumerate(spreadsheet.worksheets())]

    def get_worksheet_data(self, spreadsheet, worksheet_index):
        """Obtém dados de uma aba específica pelo índice"""
        try:
            worksheet = spreadsheet.get_worksheet(worksheet_index)
            return worksheet.get_all_values()
        except Exception as e:
            raise Exception(f"Erro ao ler aba: {str(e)}")

    def update_worksheet_with_dataframe(self, spreadsheet, worksheet_name, df):
        """
        Verifica se uma aba existe. Se sim, limpa e a preenche com os dados
        de um DataFrame. Se não, cria a aba primeiro.
        """
        print(f"Preparando para salvar dados na aba '{worksheet_name}'...")
        try:
            # Tenta selecionar a aba pelo nome
            worksheet = spreadsheet.worksheet(worksheet_name)
            print(f"Aba '{worksheet_name}' encontrada. Limpando o conteúdo existente...")
            worksheet.clear()
        except gspread.WorksheetNotFound:
            # Se a aba não for encontrada, cria uma nova
            print(f"Aba '{worksheet_name}' não encontrada. Criando uma nova aba...")
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="50")
        
        print(f"Escrevendo {len(df)} linhas na aba...")
        set_with_dataframe(worksheet, df)
        print(f"✓ Dados salvos com sucesso na planilha '{spreadsheet.title}'!")