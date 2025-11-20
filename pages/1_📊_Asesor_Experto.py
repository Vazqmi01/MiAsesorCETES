import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import tempfile
import base64

from prompts import cetes_prompt
from audiorecorder import audiorecorder
from utils.common import (
    client_openai, client_deepseek, model_deepseek,
    audio_player_with_speed, get_image_path
)

# Configuración de la página
st.set_page_config(
    page_title="Asesor Experto - Mi Asesor CETES",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("💡 Asesor Experto en CETES")
st.markdown("Chatea con un experto en CETES, Banxico e inflación.")
st.divider()

# Cargar el prompt del sistema
SYSTEM_PROMPT = cetes_prompt

# --- Lógica del Chatbot ---

# Sidebar con botón de limpiar (debe estar antes de mostrar mensajes)
with st.sidebar:
    if st.button("🗑️ Limpiar Chat"):
        # Limpiar todos los mensajes
        st.session_state.cetes_messages = []
        # Reinicializar con el disclaimer
        st.session_state.cetes_messages.append({
            "role": "assistant",
            "content": "💡 Este asistente tiene fines **educativos e informativos**. Úsalo para comprender tu perfil de riesgo y para aprender a analizar instrumentos de deuda."
        })
        st.rerun()

# Inicializar el historial si no existe
if "cetes_messages" not in st.session_state:
    st.session_state.cetes_messages = [] 
    # Añadir el disclaimer como primer mensaje
    st.session_state.cetes_messages.append({
        "role": "assistant",
        "content": "💡 Este asistente tiene fines **educativos e informativos**. Úsalo para comprender tu perfil de riesgo y para aprender a analizar instrumentos de deuda."
    })

# Mostrar mensajes antiguos en la UI
for message in st.session_state.cetes_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Reproducir audio si existe para mensajes del asistente
        if message["role"] == "assistant" and "audio_bytes" in message:
            st.markdown(audio_player_with_speed(message["audio_bytes"], 1.25), unsafe_allow_html=True)

# Sección de entrada: texto y grabación de voz
col_input, col_audio = st.columns([4, 1])

with col_input:
    user_input = st.chat_input("Escribe o graba un mensaje de voz, ¿Qué quieres saber sobre CETES?")

with col_audio:
    st.write("🎤")
    audio = audiorecorder("Grabar", "Detener")

# Procesar audio grabado (STT) - SOLO si no hay entrada de texto
if user_input is None and audio is not None and len(audio) > 0:
    try:
        # Convertir audio a formato WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            audio.export(tmp_file.name, format="wav")
            audio_path = tmp_file.name
        
        # Transcribir audio usando OpenAI Whisper
        with st.spinner("🎤 Transcribiendo audio..."):
            if client_openai:
                with open(audio_path, "rb") as audio_file:
                    transcript = client_openai.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=audio_file,
                        language="es"
                    )
                user_input = transcript.text
            else:
                st.error("❌ API Key de OpenAI no configurada para transcripción")
        
        # Limpiar archivo temporal
        os.unlink(audio_path)
        
    except Exception as e:
        st.error(f"❌ Error al transcribir audio: {e}")

# Obtener nueva entrada del usuario (texto o voz)
if user_input:
    # Mostrar y guardar el mensaje del usuario
    st.session_state.cetes_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- Lógica de API (Directa a DeepSeek para el chat) ---
    try:
        # 1. Preparar el historial para la API
        messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in st.session_state.cetes_messages:
            messages_for_api.append({"role": msg["role"], "content": msg["content"]})

        # 2. Llamar a la API de DeepSeek
        if client_deepseek:
            with st.spinner("Pensando..."):
                response = client_deepseek.chat.completions.create(
                    model=model_deepseek,
                    messages=messages_for_api
                )
                assistant_response = response.choices[0].message.content
        else:
            st.error("❌ API Key de DeepSeek no configurada")
            assistant_response = "Lo siento, no tengo acceso a la API de DeepSeek en este momento."
        
        # 3. Mostrar y guardar la respuesta del modelo
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
        # 4. Generar audio TTS siempre activo
        audio_bytes = None
        if client_openai:
            try:
                with st.spinner("🔊 Generando audio..."):
                    # Generar audio usando OpenAI TTS
                    tts_response = client_openai.audio.speech.create(
                        model="gpt-4o-mini-tts",
                        voice="shimmer",
                        input=assistant_response,
                        speed=1.25
                    )
                    audio_bytes = tts_response.content
                
                # Reproducir audio con velocidad 1.25
                st.markdown(audio_player_with_speed(audio_bytes, 1.25), unsafe_allow_html=True)
        
            except Exception as e:
                st.warning(f"⚠️ No se pudo generar audio: {e}")
        
        # Guardar mensaje con audio si existe
        message_to_save = {"role": "assistant", "content": assistant_response}
        if audio_bytes:
            message_to_save["audio_bytes"] = audio_bytes
        st.session_state.cetes_messages.append(message_to_save)

    except Exception as e:
        st.error(f"Error al generar respuesta: {e}")
