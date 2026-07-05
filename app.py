import streamlit as st
import pandas as pd
import os

FILE_NAME = 'album.csv'

# Configuração da página
st.set_page_config(page_title="Organizador 2026", layout="wide")

def carregar_dados():
    # 'on_bad_lines="skip"' ignora linhas corrompidas
    # 'sep=","' define a vírgula como separador
    # 'encoding="utf-8-sig"' lida melhor com acentos/caracteres especiais
    return pd.read_csv(FILE_NAME, sep=',', on_bad_lines='skip', encoding='utf-8-sig')

st.title("⚽ Meu Álbum 2026")

try:
    df = carregar_dados()
    
    # Validação: garantir que as colunas essenciais existem
    if 'Status' not in df.columns:
        df['Status'] = False
        df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')

    # Filtro por seleção (Sidebar)
    selecao_escolhida = st.sidebar.selectbox("Filtrar por Seleção:", df['Selecao'].unique())

    st.subheader(f"Figurinhas - {selecao_escolhida}")

    # Filtrar o DataFrame
    df_filtrado = df[df['Selecao'] == selecao_escolhida].copy()

    # Exibir figurinhas com checkbox
    for index, row in df_filtrado.iterrows():
        # Usamos o 'index' original para atualizar o dataframe principal
        orig_idx = df[df['Codigo'] == row['Codigo']].index[0]
        
        col1, col2 = st.columns([4, 1])
        col1.write(f"**{row['Codigo']}** - {row['Item']}")
        
        # O valor do checkbox vem da coluna Status
        novo_status = col2.checkbox("Tenho", value=bool(row['Status']), key=f"check_{row['Codigo']}")
        
        if novo_status != row['Status']:
            df.at[orig_idx, 'Status'] = novo_status
            df.to_csv(FILE_NAME, index=False, encoding='utf-8-sig')
            st.rerun() # Recarrega para salvar o estado visual

except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.write("Verifique se o arquivo album.csv está na mesma pasta e tem as colunas corretas.")
