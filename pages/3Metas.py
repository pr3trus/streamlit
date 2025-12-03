import streamlit as st

st.title("🎯 METAS")

if "metas" not in st.session_state:
    st.session_state.metas = {}

materia = st.text_input("Matéria para meta:")
meta = st.number_input("Horas da meta:", 1, 100, 10)

if st.button("🎯 Salvar Meta"):
    if materia:
        st.session_state.metas[materia] = meta
        st.success(f"Meta: {meta}h de {materia}")