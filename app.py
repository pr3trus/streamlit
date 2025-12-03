import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Planner de Estudos",
    page_icon="📚",
    layout="wide"
)

# Inicializa os dados (IMPORTANTE!)
if "estudos" not in st.session_state:
    st.session_state.estudos = []

if "metas" not in st.session_state:
    st.session_state.metas = {}

# Título principal
st.title("📚 MEU PLANNER DE ESTUDOS")
st.markdown("---")

# Mensagem de boas-vindas
st.write("""
### 👋 Bem-vindo ao seu organizador de estudos!

**Use o menu à esquerda para navegar:**

1. **➕ Adicionar** - Cadastre novos estudos
2. **📋 Ver Estudos** - Veja tudo o que planejou
3. **🎯 Metas** - Defina seus objetivos
4. **📊 Progresso** - Acompanhe seu desempenho

---

### 💡 Dicas rápidas:
- Tudo é salvo automaticamente
- Pode usar no celular ou computador
- Os dados ficam salvos enquanto o app estiver aberto

---

**Comece pela página '➕ Adicionar'!**
""")

# Mostra estatísticas rápidas
if st.session_state.estudos:
    total_horas = sum(e["horas"] for e in st.session_state.estudos)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Estudos", len(st.session_state.estudos))
    with col2:
        st.metric("⏱️ Horas", f"{total_horas:.1f}h")
    with col3:
        st.metric("🎯 Metas", len(st.session_state.metas))

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com Streamlit | Atualize a página para ver mudanças")