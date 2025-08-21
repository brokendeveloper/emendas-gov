import gspread

def get_google_client(credentials_path: str):
    """
    Configura e retorna o cliente Google Sheets autorizado 
    usando o caminho para o arquivo JSON de credenciais.
    """
    try:
        # gspread.service_account lida com a autenticação de forma mais direta
        client = gspread.service_account(filename=credentials_path)
        return client
    except FileNotFoundError:
        # Erro específico se o arquivo JSON não for encontrado
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado em: {credentials_path}")
    except Exception as e:
        # Erro genérico para outras falhas de autenticação
        raise Exception(f"Erro na autenticação com o Google: {str(e)}")