import streamlit as st
import pandas as pd
import os

# Nome do arquivo de dados
FILE_NAME = 'album.csv'

# Criar arquivo se não existir
if not os.path.exists(FILE_NAME):
    # Aqui você usaria o CSV que geramos anteriormente
    st.error(f"O arquivo {FILE_NAME} não foi encontrado!")
    st.stop()

# Carregar dados
def carregar_dados():
    return pd.read_csv(FILE_NAME)

# Salvar dados
def salvar_dados(df):
    df.to_csv(FILE_NAME, index=False)

st.title("⚽ Meu Álbum 2026")

df = carregar_dados()

# Garantir que a coluna 'Status' exista
if 'Status' not in df.columns:
    df['Status'] = False
    salvar_dados(df)

# Filtro por seleção
selecao = st.sidebar.selectbox("Filtrar Seleção:", df['Selecao'].unique())

st.subheader(f"Figurinhas - {selecao}")

# Filtrar o DataFrame
df_filtrado = df[df['Selecao'] == selecao].copy()

# Exibir figurinhas
for index, row in df_filtrado.iterrows():
    col1, col2 = st.columns([4, 1])
    
    # Exibe nome e código
    col1.write(f"**{row['Codigo']}** - {row['Item']}")
    
    # Checkbox para marcar (o valor inicial vem do CSV)
    marcado = col2.checkbox("Tenho", value=row['Status'], key=str(row['Codigo']))
    
    # Se mudar o checkbox, atualiza o dataframe e salva
    if marcado != row['Status']:
        df.loc[df['Codigo'] == row['Codigo'], 'Status'] = marcado
        salvar_dados(df)

st.sidebar.success("Progresso salvo automaticamente!")
