import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Organizador de Figurinhas 2026", layout="wide")

# Inicialização dos dados (exemplo simplificado)
# Na prática, você carregaria isso de um arquivo CSV ou JSON
if 'figurinhas' not in st.session_state:
    # Simulando um álbum (IDs de BRA1 a BRA20, etc)
    all_stickers = [f"SEL{i:03d}" for i in range(1, 501)] 
    st.session_state.figurinhas = {s: {"possuo": 0, "repetidas": 0} for s in all_stickers}

def update_sticker(id, change_type, value):
    if change_type == "possuo":
        st.session_state.figurinhas[id]["possuo"] = max(0, st.session_state.figurinhas[id]["possuo"] + value)
    else:
        st.session_state.figurinhas[id]["repetidas"] = max(0, st.session_state.figurinhas[id]["repetidas"] + value)

# Abas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumo", "📝 Adicionar/Remover", "🔄 Repetidas", "🔍 Minha Coleção"])

with tab1:
    st.title("Resumo da Coleção")
    total = len(st.session_state.figurinhas)
    possuidas = sum(1 for v in st.session_state.figurinhas.values() if v["possuo"] > 0)
    progresso = (possuidas / total) * 100
    
    st.metric("Total de Figurinhas", total)
    st.metric("Restam", total - possuidas)
    st.progress(progresso / 100)
    st.write(f"Porcentagem do álbum: {progresso:.2f}%")

with tab2:
    st.title("Gerenciar Figurinhas")
    sticker_id = st.selectbox("Selecione a figurinha:", list(st.session_state.figurinhas.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar (Álbum)"): update_sticker(sticker_id, "possuo", 1)
        if st.button("Remover (Álbum)"): update_sticker(sticker_id, "possuo", -1)
    with col2:
        if st.button("Adicionar (Repetida)"): update_sticker(sticker_id, "repetidas", 1)
        if st.button("Remover (Repetida)"): update_sticker(sticker_id, "repetidas", -1)

with tab3:
    st.title("Minhas Repetidas")
    repetidas = {k: v["repetidas"] for k, v in st.session_state.figurinhas.items() if v["repetidas"] > 0}
    df_rep = pd.DataFrame.from_dict(repetidas, orient='index', columns=['Quantidade'])
    st.table(df_rep)

with tab4:
    st.title("Visualização Completa")
    df = pd.DataFrame.from_dict(st.session_state.figurinhas, orient='index')
    st.dataframe(df, use_container_width=True)
