import streamlit as st
import pandas as pd

st.set_page_config(page_title="Organizador Oficial 2026", layout="wide")

# Carrega os dados reais do seu arquivo local
@st.cache_data
def carregar_album():
    try:
        return pd.read_csv("album.csv")
    except:
        st.error("Erro: O arquivo 'album.csv' não foi encontrado na pasta!")
        return pd.DataFrame(columns=['id', 'nome', 'categoria'])

df = carregar_album()

# Inicializa o controle se não existir
if 'colecao' not in st.session_state:
    st.session_state.colecao = {
        row['id']: {"possuo": False, "repetidas": 0} 
        for _, row in df.iterrows()
    }

# Interface
st.title("⚽ Meu Álbum da Copa 2026")

tabs = st.tabs(["📊 Painel", "➕ Adicionar/Remover", "🔄 Repetidas", "📋 Checklist"])

with tabs[0]: # Painel
    tenho = sum(1 for item in st.session_state.colecao.values() if item["possuo"])
    st.metric("Total no Álbum", len(df))
    st.metric("Colecionadas", tenho)
    st.progress(tenho / len(df))

with tabs[1]: # Adicionar/Remover
    cat = st.selectbox("Categoria:", df['categoria'].unique())
    for _, row in df[df['categoria'] == cat].iterrows():
        id_f = row['id']
        c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
        c1.write(f"**{id_f}**")
        c2.write(row['nome'])
        
        # Checkbox e Input Real
        st.session_state.colecao[id_f]["possuo"] = c3.checkbox("Tenho", value=st.session_state.colecao[id_f]["possuo"], key=f"p_{id_f}")
        st.session_state.colecao[id_f]["repetidas"] = c4.number_input("Rep", min_value=0, value=st.session_state.colecao[id_f]["repetidas"], key=f"r_{id_f}")

with tabs[2]: # Repetidas
    st.table(pd.DataFrame([
        {"ID": k, "Qtd": v["repetidas"]} for k, v in st.session_state.colecao.items() if v["repetidas"] > 0
    ]))

with tabs[3]: # Checklist
    st.dataframe(df, use_container_width=True)
