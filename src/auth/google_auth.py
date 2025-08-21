import gspread

def get_google_client(credentials_path: str):
    """
    Configura e retorna o cliente Google Sheets autorizado 
    usando o caminho para o arquivo JSON de credenciais.
    """
    try:
        
        client = gspread.service_account(filename=credentials_path)
        return client
    except FileNotFoundError:
        
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {credentials_path}")
    except Exception as e:
        
        raise Exception(f"Erro na autenticação com o Google: {str(e)}")