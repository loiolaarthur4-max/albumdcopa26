import streamlit as st
import pandas as pd

st.set_page_config(page_title="Organizador Copa 2026", layout="wide")

# --- CARREGAR DADOS ---
# Se o arquivo CSV não existir, criamos um exemplo básico
try:
    df_base = pd.read_csv("figurinhas.csv")
except:
    # Apenas para o código rodar caso você ainda não tenha o CSV
    data = {"id": ["BRA01", "FWC01", "COCA01"], "nome": ["Alisson", "Logo", "Gold"], "categoria": ["BRASIL", "ESPECIAIS", "COCA-COLA"]}
    df_base = pd.DataFrame(data)

if 'album' not in st.session_state:
    st.session_state.album = {row['id']: {"nome": row['nome'], "cat": row['categoria'], "possui": False, "rep": 0} 
                              for _, row in df_base.iterrows()}

# --- FUNÇÕES ---
def salvar_mudanca(): pass # Aqui você pode adicionar lógica de salvar em banco ou Google Sheets

# --- INTERFACE ---
st.title("🏆 Organizador Oficial Copa 2026")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumo", "➕ Minhas Figurinhas", "🔄 Repetidas", "📋 Checklist"])

# Converter estado para DF
df = pd.DataFrame.from_dict(st.session_state.album, orient='index')

with tab1:
    col1, col2, col3 = st.columns(3)
    tenho = df['possui'].sum()
    col1.metric("Total no Álbum", len(df))
    col2.metric("Já Colecionadas", tenho)
    col3.metric("Porcentagem", f"{(tenho/len(df))*100:.1f}%")

with tab2:
    cat = st.selectbox("Selecione a Categoria:", df['cat'].unique())
    filtro = df[df['cat'] == cat]
    
    for id_fig, row in filtro.iterrows():
        c1, c2, c3, c4 = st.columns([1, 3, 2, 2])
        c1.write(f"**{id_fig}**")
        c2.write(row['nome'])
        
        if c3.checkbox("Possuo", value=row['possui'], key=f"p_{id_fig}"):
            st.session_state.album[id_fig]['possui'] = True
        else:
            st.session_state.album[id_fig]['possui'] = False
            
        st.session_state.album[id_fig]['rep'] = c4.number_input("Rep", min_value=0, value=row['rep'], key=f"r_{id_fig}")

with tab3:
    st.subheader("Minhas Repetidas")
    st.dataframe(df[df['rep'] > 0][['nome', 'rep']])

with tab4:
    st.dataframe(df, use_container_width=True)
