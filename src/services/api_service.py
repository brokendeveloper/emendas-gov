import pandas as pd
import requests

class ApiService:
    def __init__(self):
        
        self.base_url = "https://api.transferegov.gestao.gov.br/transferenciasespeciais"

    def fetch_and_process_data(self):
        
        CNPJ_PE = "10571982000125"

        # --- ETAPA 1: Buscar os Planos de Ação ---
        print("1. Buscando Planos de Ação...")
        try:
            url_planos = f"{self.base_url}/plano_acao_especial"
            params_planos = {"cnpj_beneficiario_plano_acao": f"eq.{CNPJ_PE}"}
            response = requests.get(url_planos, params=params_planos)
            response.raise_for_status()
            df_planos = pd.DataFrame(response.json())
            if df_planos.empty:
                raise Exception("Nenhum Plano de Ação encontrado para o CNPJ fornecido.")
            print(f"✓ {len(df_planos)} Planos de Ação encontrados.")
        except Exception as e:
            raise Exception(f"Erro ao buscar Planos de Ação: {e}")

        ids_planos_acao = df_planos['id_plano_acao'].tolist()
        ids_str = ",".join(str(i) for i in ids_planos_acao)

        # --- ETAPA 2: Buscar os Executores ---
        print("2. Buscando Executores dos planos...")
        try:
            url_executores = f"{self.base_url}/executor_especial"
            params_executores = {"id_plano_acao": f"in.({ids_str})"}
            response = requests.get(url_executores, params=params_executores)
            response.raise_for_status()
            df_executores = pd.DataFrame(response.json())
            print(f"✓ {len(df_executores)} registros de Executores encontrados.")
        except Exception as e:
            raise Exception(f"Erro ao buscar Executores: {e}")

        # --- ETAPA 3: Buscar os Planos de Trabalho ---
        print("3. Buscando Planos de Trabalho...")
        try:
            url_trabalho = f"{self.base_url}/plano_trabalho_especial"
            params_trabalho = {"id_plano_acao": f"in.({ids_str})"}
            response = requests.get(url_trabalho, params=params_trabalho)
            response.raise_for_status()
            df_planos_trabalho = pd.DataFrame(response.json())
            print(f"✓ {len(df_planos_trabalho)} Planos de Trabalho encontrados.")
        except Exception as e:
            raise Exception(f"Erro ao buscar Planos de Trabalho: {e}")

        # --- ETAPA 4: Unir as tabelas (Merge) ---
        print("4. Unindo as tabelas de dados...")
        # Merge 1: trabalho + plano
        df_merged = df_planos_trabalho.merge(
            df_planos, on="id_plano_acao", how="left", suffixes=('_trabalho', '_plano')
        )
        # Merge 2: com executor
        df_merged = df_merged.merge(
            df_executores, on="id_plano_acao", how="left", suffixes=('', '_executor')
        )
        print("✓ Tabelas unidas com sucesso!")

         # --- ETAPA 5: Filtrar e Renomear as colunas de interesse ---
        print("5. Filtrando e formatando o relatório final...")
        
        colunas_de_interesse = [
            'situacao_plano_trabalho', 'data_inicio_execucao_plano_trabalho',
            'data_fim_execucao_plano_trabalho', 'codigo_plano_acao', 'situacao_plano_acao',
            'cnpj_beneficiario_plano_acao', 'nome_beneficiario_plano_acao', 'numero_conta_plano_acao',
            'nome_parlamentar_emenda_plano_acao', 'ano_emenda_parlamentar_plano_acao',
            'numero_emenda_parlamentar_plano_acao', 'codigo_descricao_areas_politicas_publicas_plano_acao',
            'motivo_impedimento_plano_acao', 'valor_custeio_plano_acao', 'valor_investimento_plano_acao',
            'cnpj_executor', 'nome_executor', 'objeto_executor', 'vl_custeio_executor',
            'vl_investimento_executor', 'numero_conta_executor',
        ]

        df_filtrado = df_merged[colunas_de_interesse]
        df_renomeado = df_filtrado.rename(columns={
            'situacao_plano_trabalho': 'Situação do Plano de Trabalho',
            'data_inicio_execucao_plano_trabalho': 'Início da Execução',
            'data_fim_execucao_plano_trabalho': 'Fim da Execução',
            'codigo_plano_acao': 'Código do Plano de Ação',
            'situacao_plano_acao': 'Situação do Plano de Ação',
            'cnpj_beneficiario_plano_acao': 'CNPJ Beneficiário',
            'nome_beneficiario_plano_acao': 'Nome Beneficiário',
            'numero_conta_plano_acao': 'Nº Conta Plano de Ação',
            'nome_parlamentar_emenda_plano_acao': 'Nome do Parlamentar',
            'ano_emenda_parlamentar_plano_acao': 'Ano da Emenda',
            'numero_emenda_parlamentar_plano_acao': 'Nº da Emenda',
            'codigo_descricao_areas_politicas_publicas_plano_acao': 'Descrição da Política Pública',
            'motivo_impedimento_plano_acao': 'Motivo do Impedimento',
            'valor_custeio_plano_acao': 'Valor de Custeio (Plano)',
            'valor_investimento_plano_acao': 'Valor de Investimento (Plano)',
            'cnpj_executor': 'CNPJ do Executor',
            'nome_executor': 'Nome do Executor',
            'objeto_executor': 'Objeto do Executor',
            'vl_custeio_executor': 'Valor de Custeio (Executor)',
            'vl_investimento_executor': 'Valor de Investimento (Executor)',
            'numero_conta_executor': 'Nº Conta do Executor'
        })

        # --- ETAPA 6: Padronizar e Formatar Colunas Numéricas ---
        print("6. Padronizando colunas de valores...")
        
        colunas_de_valor = [
            'Valor de Custeio (Plano)',
            'Valor de Investimento (Plano)',
            'Valor de Custeio (Executor)',
            'Valor de Investimento (Executor)'
        ]

        for coluna in colunas_de_valor:
            if coluna in df_renomeado.columns:
                df_renomeado[coluna] = df_renomeado[coluna].fillna(0).round(0).astype(int)
        
        df_final = df_renomeado

        print("✓ DataFrame final gerado e formatado com sucesso!")
        return df_final
