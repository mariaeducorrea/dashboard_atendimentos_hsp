import pandas as pd

# Leitura do CSV
caminho_csv = 'C:/Users/Administrador/Desktop/projetos/dashboard_atendimentos_hsp/dados/dados.csv'
dados = pd.read_csv(caminho_csv)


dados['id_registro'] = dados.index + 1

# Converter datas e horas
dados['data_atendimento'] = pd.to_datetime(dados['data_atendimento'] + ' ' + dados['hora_inicio'])
dados['data_alta'] = pd.to_datetime(dados['data_alta'] + ' ' + dados['hora_fim'])
dados['data'] = pd.to_datetime(dados['data_atendimento']).dt.date


# Arredondar hora 
dados['hora_inicio_arred'] = dados['data_atendimento'].dt.floor('h').dt.strftime('%H:00')
dados['hora_fim_arred'] = dados['data_alta'].dt.floor('h').dt.strftime('%H:00')

# Extrair idade
dados['anos'] = dados['idade_paciente'].str.extract(r'(\d+)\s*ano')[0].fillna(0).astype(int)
dados['meses'] = dados['idade_paciente'].str.extract(r'(\d+)\s*mês')[0].fillna(0).astype(int)
dados['dias'] = dados['idade_paciente'].str.extract(r'(\d+)\s*dias?')[0].fillna(0).astype(int)
dados['idade_dias'] = (dados['anos'] * 365) + (dados['meses'] * 30) + dados['dias']

# Categorização de idade
def categorizar_idade(dias):
    if dias < 365:
        return 'Bebê (0-11 meses)'
    elif dias < 11 * 365:
        return 'Criança (1-11 anos)'
    elif dias < 17 * 365:
        return 'Adolescente (12-17 anos)'
    elif dias < 59 * 365:
        return 'Adulto (18-59 anos)'
    else:
        return 'Idoso (60+ anos)'
dados['categoria_idade'] = dados['idade_dias'].apply(categorizar_idade)

# Cálculo da duração em horas
dados['duracao_horas'] = (dados['data_alta'] - dados['data_atendimento']).dt.total_seconds() / 3600

# Categorização de tempo de permanência
def categorizar_permanencia(horas):
    if horas < 24:
        return 'Menos de 24h'
    elif horas < 72:
        return '1 a 2 dias'
    elif horas < 120:
        return '3 a 4 dias'
    elif horas < 240:
        return '5 a 10 dias'
    else:
        return 'Mais de 10 dias'
dados['categoria_permanencia'] = dados['duracao_horas'].apply(categorizar_permanencia)

dados['quantidade'] = 1

Atendimentos = [
    'id_registro', 
    'data',
    'hora_inicio_arred', 
    'convenio', 
    'unidade', 
    'setor',
    'tipo_atendimento', 
    'categoria_idade', 
    'categoria_permanencia',
    'quantidade'
]

dados_atendimentos = dados[Atendimentos]

print(dados_atendimentos)



caminho_saida_xlsx = 'C:/Users/Administrador/Desktop/projetos/dashboard_atendimentos_hsp/dados/dados.xlsx'
with pd.ExcelWriter(caminho_saida_xlsx, engine='openpyxl') as writer:
    dados_atendimentos.to_excel(writer, sheet_name='Dados Transformados', index=False)


print("Processamento concluído. Arquivo salvo em:", caminho_saida_xlsx)
