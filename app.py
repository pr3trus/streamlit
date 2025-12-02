import streamlit as st
import pandas as pd
from datetime import datetime

def preparar_memoria():
    """Inicializa as variáveis de sessão para persistência de dados"""
    if "lista_estudos" not in st.session_state:
        st.session_state.lista_estudos = []
    
    if "lista_metas" not in st.session_state:
        st.session_state.lista_metas = {}

def adicionar_estudo(materia, dia, horario, tempo, prioridade):
    """Adiciona um novo estudo à lista de estudos"""
    st.session_state.lista_estudos.append({
        "Matéria": materia,
        "Dia": dia,
        "Horário": horario,
        "Tempo(horas)": tempo,
        "Prioridade": prioridade
    })

def criar_tabela():
    """Cria um DataFrame pandas com todos os estudos cadastrados"""
    if len(st.session_state.lista_estudos) == 0:
        return pd.DataFrame(columns=["Matéria", "Dia", "Horário", "Tempo(horas)", "Prioridade"])
    return pd.DataFrame(st.session_state.lista_estudos)

def calcular_horas_totais(tabela):
    """Calcula o total de horas estudadas por matéria"""
    if tabela.empty:
        return pd.DataFrame(columns=["Matéria", "Tempo(horas)"])
    return tabela.groupby("Matéria", as_index=False)["Tempo(horas)"].sum()

def salvar_meta(materia, meta):
    """Salva a meta de horas para uma matéria específica"""
    st.session_state.lista_metas[materia] = meta

def pegar_meta(materia):
    """Recupera a meta de horas de uma matéria (retorna 0 se não existir)"""
    return st.session_state.lista_metas.get(materia, 0)

def exportar_csv(tabela):
    """Exporta a tabela de estudos para CSV"""
    if not tabela.empty:
        csv = tabela.to_csv(index=False, encoding='utf-8')
        return csv
    return None

def exportar_totais_csv(tabela_totais):
    """Exporta a tabela de totais para CSV"""
    if not tabela_totais.empty:
        csv = tabela_totais.to_csv(index=False, encoding='utf-8')
        return csv
    return None


st.set_page_config(
    page_title="Planner de Estudos",
    page_icon="📚",
    layout="wide"
)


st.title("📚 Planner de Estudos")
st.markdown("---")


preparar_memoria()


with st.sidebar:
    st.header("⚙️ Configurações")
    

    st.subheader("📤 Exportar Dados")
    tabela = criar_tabela()
    
    if not tabela.empty:
        csv_estudos = exportar_csv(tabela)
        if csv_estudos:
            st.download_button(
                label="📥 Exportar Estudos (CSV)",
                data=csv_estudos,
                file_name=f"estudos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        tabela_totais = calcular_horas_totais(tabela)
        csv_totais = exportar_totais_csv(tabela_totais)
        if csv_totais:
            st.download_button(
                label="📊 Exportar Totais (CSV)",
                data=csv_totais,
                file_name=f"totais_estudos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    else:
        st.info("Nenhum dado para exportar")
    
    st.markdown("---")
    st.subheader("📊 Estatísticas")
    if not tabela.empty:
        st.metric("Total de Estudos", len(tabela))
        st.metric("Total de Horas", f"{tabela['Tempo(horas)'].sum():.1f}h")
        st.metric("Matérias Diferentes", tabela['Matéria'].nunique())


col1, col2 = st.columns([2, 1])

with col1:
    st.header("➕ Adicionar Novo Estudo")
    
    with st.form("form_estudo", clear_on_submit=True):

        materia = st.text_input("Matéria:*", placeholder="Ex: Matemática, Física...")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            dia = st.selectbox("Dia da Semana:*", 
                              ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
            horario = st.text_input("Horário:*", placeholder="Ex: 14:00")
        
        with col_form2:
            tempo = st.number_input("Tempo de estudo (horas):*", 
                                   min_value=0.5, 
                                   step=0.5, 
                                   value=1.0)
            prioridade = st.selectbox("Prioridade:*", 
                                     ["Alta", "Média", "Baixa"])
        
        botao = st.form_submit_button("✅ Adicionar Estudo")
        
        if botao:
            if materia and horario:
                adicionar_estudo(materia, dia, horario, tempo, prioridade)
                st.success("🎉 Estudo adicionado com sucesso!")
            else:
                st.error("❌ Por favor, preencha todos os campos obrigatórios (*)")

with col2:
    st.header("🎯 Definir Metas")
    
    materia_meta = st.text_input("Matéria para meta:", 
                                placeholder="Nome da matéria",
                                key="materia_meta")
    meta_horas = st.number_input("Meta de horas:", 
                                min_value=0.0, 
                                step=0.5, 
                                value=5.0,
                                key="meta_horas")
    
    if st.button("💾 Salvar Meta", use_container_width=True):
        if materia_meta:
            salvar_meta(materia_meta, meta_horas)
            st.success(f"🎯 Meta de {meta_horas} horas salva para {materia_meta}!")
        else:
            st.error("❌ Digite o nome da matéria")


st.markdown("---")
st.header("📋 Seus Estudos Agendados")


tabela = criar_tabela()
if not tabela.empty:

    ordem_dias = {"Segunda": 1, "Terça": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5, "Sábado": 6, "Domingo": 7}
    tabela['Ordem'] = tabela['Dia'].map(ordem_dias)
    tabela = tabela.sort_values(['Ordem', 'Horário']).drop('Ordem', axis=1)
    
    st.dataframe(tabela, use_container_width=True)
    
  
    if st.button("🗑️ Limpar Todos os Estudos", type="secondary"):
        st.session_state.lista_estudos = []
        st.rerun()
else:
    st.info("📝 Nenhum estudo adicionado ainda. Use o formulário acima para começar!")


if not tabela.empty:
    st.markdown("---")
    st.header("📊 Progresso das Matérias")
    
    tabela_totais = calcular_horas_totais(tabela)
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.subheader("📈 Totais por Matéria")
        st.dataframe(tabela_totais, use_container_width=True)
    
    with col_stat2:
        st.subheader("🎯 Metas e Progresso")
        
        for index, row in tabela_totais.iterrows():
            materia = row["Matéria"]
            total = row["Tempo(horas)"]
            meta = pegar_meta(materia)
            
            if meta > 0:
                progresso = min(total / meta, 1.0)
                porcentagem = progresso * 100
                
                st.write(f"**{materia}**")
                st.write(f"{total:.1f}h / {meta:.1f}h ({porcentagem:.1f}%)")
                st.progress(progresso)
                
                if progresso >= 1.0:
                    st.success("🎉 Meta concluída!")
                elif progresso >= 0.75:
                    st.info("👍 Quase lá!")
                elif progresso >= 0.5:
                    st.warning("📚 Continue assim!")
                else:
                    st.error("📖 Precisa estudar mais")
                
                st.markdown("---")
            else:
                st.write(f"**{materia}**: {total:.1f}h")
                st.info("ℹ️ Meta não definida")
                st.markdown("---")
    
    with col_stat3:
        st.subheader("📅 Distribuição por Dia")
        
        estudos_por_dia = tabela['Dia'].value_counts()
        st.bar_chart(estudos_por_dia)
        
        st.subheader("🎯 Distribuição por Prioridade")
        prioridades_contagem = tabela['Prioridade'].value_counts()
        st.dataframe(prioridades_contagem, use_container_width=True)


st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "📚 Planner de Estudos - Desenvolvido com Streamlit"
    "</div>",
    unsafe_allow_html=True
)