import streamlit as st
import requests
from io import BytesIO

# Título e cabeçalho
st.title("🚀 Personalized Pathway Report 🚀")
st.markdown("### Find the Fastest Path to Your Dream Career!")

# Upload do logo
st.image("https://cdn.prod.website-files.com/65cd787b996708ed6404fc40/65e13f8434ed5dc4c2d48c89_university-startup-logo-horiz-TM-med.png", width=300)

# Caixa de diálogo para respostas
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.write("### Chat History")
chat_container = st.container()

# Alternar entre áudio e texto
use_audio_response = st.checkbox("Enable Audio Response", value=False)

# Entrada de perguntas
question = st.text_input("Type your question here")

# Botões
if st.button("Send"):
    if question.strip():
        st.session_state["chat_history"].append(("You", question))

        # Rota da API
        route = "/response-audio" if use_audio_response else "/response"

        # Exemplo de chamada à API (ajuste a URL base)
        api_url = f"http://localhost:5000{route}"
        response = requests.post(api_url, data={"question": question})

        if response.status_code == 200:
            data = response.json()
            if use_audio_response:
                audio_url = data.get("audio_url")
                if audio_url:
                    audio_response = requests.get(audio_url)
                    audio_bytes = BytesIO(audio_response.content)
                    st.audio(audio_bytes, format="audio/mpeg")
            else:
                answer = data.get("response", "No response")
                st.session_state["chat_history"].append(("Assistant", answer))
        else:
            st.error("Error fetching response from the server.")

# Exibir histórico do chat
with chat_container:
    for speaker, message in st.session_state["chat_history"]:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"_**{speaker}:** {message}_")

# Resetar conversa
if st.button("New Chat"):
    st.session_state["chat_history"] = []
    st.success("Chat reset successfully!")

# Reconhecimento de voz (não suportado diretamente no Streamlit, mas explicado para manter contexto)
st.info("Speech recognition isn't natively supported in Streamlit. For similar functionality, integrate with an external service.")
