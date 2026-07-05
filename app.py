import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gerenciador Copa 2026", layout="wide")

# Carrega os dados reais do seu arquivo CSV
@st.cache_data
def load_data():
    return pd.read_csv("figurinhas.csv") # O arquivo deve estar na mesma pasta

df = load_data()

# Inicializa o estado das 994 figurinhas
if 'meu_album' not in st.session_state:
    st.session_state.meu_album = {
        row['id']: {"possuo": False, "repetidas": 0} 
        for _, row in df.iterrows()
    }

st.title("🏆 Gerenciador Oficial: 994 Figurinhas")

# Abas
aba1, aba2, aba3, aba4 = st.tabs(["📊 Resumo", "📝 Adicionar/Remover", "🔄 Repetidas", "📋 Checklist"])

# Cálculo de progresso
total = len(df)
tenho = sum(1 for item in st.session_state.meu_album.values() if item["possuo"])

with aba1:
    st.metric("Total de Figurinhas", total)
    st.metric("Já Colecionadas", tenho)
    st.progress(tenho / total)
    st.write(f"Faltam: {total - tenho}")

with aba2:
    categoria = st.selectbox("Escolha a Seleção ou Categoria:", df['categoria'].unique())
    subset = df[df['categoria'] == categoria]
    
    for _, row in subset.iterrows():
        id_fig = row['id']
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        c1.write(f"**{id_fig}**")
        c2.write(row['nome'])
        
        # Checkbox para possuir
        st.session_state.meu_album[id_fig]["possuo"] = c3.checkbox("Tenho", value=st.session_state.meu_album[id_fig]["possuo"], key=f"p_{id_fig}")
        
        # Contador de repetidas
        st.session_state.meu_album[id_fig]["repetidas"] = c4.number_input("Rep", min_value=0, value=st.session_state.meu_album[id_fig]["repetidas"], key=f"r_{id_fig}")

with aba3:
    st.header("Suas Repetidas")
    rep_data = []
    for id_fig, val in st.session_state.meu_album.items():
        if val["repetidas"] > 0:
            nome = df[df['id'] == id_fig]['nome'].values[0]
            rep_data.append({"ID": id_fig, "Nome": nome, "Qtd": val["repetidas"]})
    
    if rep_data:
        st.table(pd.DataFrame(rep_data))
    else:
        st.write("Nenhuma repetida no momento.")

with aba4:
    st.dataframe(df, use_container_width=True)
