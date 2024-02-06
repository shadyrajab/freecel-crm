import pandas as pd 
from io import StringIO
import json
from requests import request
from dotenv import load_dotenv 
from os import getenv

load_dotenv()

ESTRUTURA = getenv('tokenEstrutura')
USUARIO = getenv('tokenUsuario')
URL = 'https://app.neosales.com.br/producao-painel-integration-v2'

def to_data_frame(response) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(
            StringIO(response.text), sep=';', header=0, encoding='utf-8'
        )

        # Remover colunas desnecessárias
        columns_to_drop = [
            'Pedido Vinculado',
            'Usuário ADM',
            'Revisão',
            'Item',
            'Data Instalação',
            'Período',
            'Cidade Instalação',
            'Estado Instalação',
            'Rpon',
            'Instância',
            'Consultor na Operadora',
            'Etapa Item'
        ]
        dataframe = dataframe.drop(columns=columns_to_drop, axis=1)

        # Converter todas as colunas para string
        dataframe = dataframe.astype(str)

        return dataframe

    except Exception as e:
        print(f"Erro ao processar resposta: {e}")
        return None

def get_crm_panel(dataHoraInicioCarga, dataHoraFimCarga) -> pd.DataFrame:
    payload = {
        "tokenEstrutura": ESTRUTURA,
        "tokenUsuario": USUARIO,
        "dataHoraInicioCarga": dataHoraInicioCarga,
        "dataHoraFimCarga": dataHoraFimCarga,
        "painelId": "15316",
        "outputFormat": "csv"
    }

    payload = json.dumps(payload)

    headers = {
        'Content-Type': 'text/plain',
        'Cookie': '__cflb=02DiuHcRebXBbQZs3gX28EM2MeLsdaT3jC2MMTm36LJzp'
    }

    response = request('GET', url=URL, data=payload, headers=headers)

    if response.status_code == 200:
        dataframe = to_data_frame(response)
        return dataframe
    
    else:
        print(f"Erro ao obter dados: Código de status {response.status_code}")
        return None