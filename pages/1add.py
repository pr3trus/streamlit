import streamlit as st

st.title("➕ ADICIONAR ESTUDO")

if "estudos" not in st.session_state:
    st.session_state.estudos = []

materia = st.text_input("Matéria:")
horas = st.slider("Horas:", 0.5, 4.0, 1.0, 0.5)
dia = st.selectbox("Dia:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])

if st.button("💾 Salvar"):
    if materia:
        estudo = {"materia": materia, "horas": horas, "dia": dia}
        st.session_state.estudos.append(estudo)
        st.success(f"✅ {materia} salvo!")