import vertexai
import streamlit as st
import os
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter credenciais do projeto
project_id = os.getenv("PROJECT_ID")
project_region = os.getenv("REGION")

# Verificar se as variáveis foram carregadas corretamente
if not project_id or not project_region:
    st.error("Erro: As variáveis de ambiente PROJECT_ID e REGION não foram carregadas.")
    st.stop()

# Autenticar com Vertex AI
vertexai.init(project=project_id, location=project_region)

# Carregar o modelo
model = GenerativeModel("gemini-1.0-pro")


def user_interfaces():
    # Configurações da página
    st.set_page_config(
        page_title="VertexAI Chat 🧠",
        page_icon="🤖",
        layout="centered"
    )
    
    # CSS customizado
    st.markdown("""
    <style>
        .stTextInput>div>div>input {
            border-radius: 20px;
            padding: 10px 15px;
        }
        .stButton>button {
            border-radius: 20px;
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
        }
        .stMarkdown {
            padding: 15px;
            border-radius: 10px;
            background-color: #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Layout principal
    st.title("Vertex AI Chat 🤖")
    st.markdown("**Converse com o modelo Gemini 1.0 Pro**")
    
    # Inicializar histórico de conversa
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Exibir histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adicionar mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Resposta do assistente
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Gerando resposta..."):
                try:
                    response = model.generate_content(prompt)
                    full_response = response.text
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {str(e)}")
                    full_response = "Desculpe, ocorreu um erro ao processar sua solicitação."
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    user_interfaces()
