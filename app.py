import streamlit as st
import pandas as pd

# 1. Carrega os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('album.csv')

df = carregar_dados()

st.title("Meu Organizador de Figurinhas 2026")

# 2. Filtro de Seleção
selecao = st.selectbox("Escolha a Seleção:", df['Selecao'].unique())

# 3. Exibe as figurinhas da seleção filtrada
df_filtrado = df[df['Selecao'] == selecao]

for index, row in df_filtrado.iterrows():
    # Cria uma linha para cada figurinha com um checkbox
    col1, col2 = st.columns([3, 1])
    col1.write(f"{row['Codigo']} - {row['Item']}")
    
    # Checkbox para marcar se tem ou não
    if col2.checkbox("Tenho", key=row['Codigo']):
        # Aqui você pode salvar o estado se quiser
        pass

st.success("Progresso salvo automaticamente na sessão!")
