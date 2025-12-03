import streamlit as st
import pandas as pd

st.title("📅 AGENDA DA SEMANA")

if "estudos" not in st.session_state or not st.session_state.estudos:
    st.info("📭 Nenhum estudo agendado ainda.")
else:
    # Ordem dos dias
    ordem_dias = {
        "Segunda": 1, "Terça": 2, "Quarta": 3, 
        "Quinta": 4, "Sexta": 5, "Sábado": 6, "Domingo": 7
    }
    
    # Cria DataFrame
    df = pd.DataFrame(st.session_state.estudos)
    
    # Ordena por dia
    df['ordem'] = df['dia'].map(ordem_dias)
    df = df.sort_values(['ordem', 'materia'])
    
    # Tabela organizada por dia
    st.subheader("📋 Estudos Agendados")
    
    for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]:
        estudos_dia = df[df['dia'] == dia]
        
        if not estudos_dia.empty:
            st.write(f"### 📅 {dia}")
            
            for _, estudo in estudos_dia.iterrows():
                # Ícone de prioridade
                if estudo['prioridade'] == "Alta":
                    prioridade_icon = "🔴"
                elif estudo['prioridade'] == "Média":
                    prioridade_icon = "🟡"
                else:
                    prioridade_icon = "🟢"
                
                st.write(f"{prioridade_icon} **{estudo['materia']}**")
                st.write(f"   ⏰ {estudo['horas']}h | Prioridade: {estudo['prioridade']}")
                st.write("---")