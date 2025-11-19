import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import tempfile
import io
import base64

# Importa tu prompt
from prompts import cetes_prompt
from audiorecorder import audiorecorder

# --- 1. Carga de Claves y Modelos ---
load_dotenv(override=True)
# OpenAI API para TTS y STT
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# DeepSeek API para el chat
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Inicializar clientes
client_openai = OpenAI(api_key=OPENAI_API_KEY)  # Para TTS y STT
client_deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)  # Para chat

# Nombres de los modelos
model_deepseek = "deepseek-chat"

# --- 3. Carga del Prompt de Sistema ---
SYSTEM_PROMPT = cetes_prompt

# Configuración de la página
st.set_page_config(
    page_title="Mi Asesor CETES",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_image_path(filename):
    """Obtiene la ruta de una imagen local"""
    image_dir = Path("images")
    if image_dir.exists():
        image_path = image_dir / filename
        if image_path.exists():
            return str(image_path)
    return None

def audio_player_with_speed(audio_bytes, playback_speed=1.25):
    """Crea un reproductor de audio con velocidad de reproducción personalizada"""
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    audio_html = f"""
    <audio controls id="audioPlayer" style="width: 100%;">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    <script>
        var audio = document.getElementById('audioPlayer');
        audio.playbackRate = {playback_speed};
        // Asegurar que se aplique cuando se carga el audio
        audio.addEventListener('loadedmetadata', function() {{
            audio.playbackRate = {playback_speed};
        }});
    </script>
    """
    return audio_html

# Sección de bienvenida con imagen
st.header("🏡 Bienvenido")
col1, col2 = st.columns([2, 1])

with col1:
    st.write("""
    **Mi Asesor CETES** es tu herramienta inteligente para realizar pronósticos y análisis 
    de los Certificados de la Tesorería de la Federación (CETES). 
    
    Con esta aplicación podrás:
    - 📊 Analizar tendencias históricas de CETES
    - 📈 Realizar pronósticos de tasas de interés
    - 💡 Tomar decisiones de inversión informadas
    - 📉 Visualizar gráficos interactivos
    """)

with col2:
    logo_path = get_image_path("Logo.png")
    if logo_path:
        st.image(logo_path, width=250)

st.markdown("---")

st.header("💡 Asesor Experto en CETES")
st.markdown("Chatea con un experto en CETES, Banxico e inflación.")
st.divider()

# --- Lógica del Chatbot ---

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
            with open(audio_path, "rb") as audio_file:
                transcript = client_openai.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=audio_file,
                    language="es"
                )
        
        user_input = transcript.text
        #st.info(f"🎤 **Dijiste:** {user_input}")
        
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
        # 1. Preparar el historial para la API - solo incluir role y content
        messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Filtrar solo los campos necesarios (role y content) para evitar problemas de serialización
        for msg in st.session_state.cetes_messages:
            messages_for_api.append({"role": msg["role"], "content": msg["content"]})

        # 2. Llamar a la API de DeepSeek
        with st.spinner("Pensando..."):
            response = client_deepseek.chat.completions.create(
                model=model_deepseek,
                messages=messages_for_api
            )
            
            assistant_response = response.choices[0].message.content
        
        # 3. Mostrar y guardar la respuesta del modelo
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
        # 4. Generar audio TTS siempre activo
        audio_bytes = None
        if OPENAI_API_KEY:
            try:
                with st.spinner("🔊 Generando audio..."):
                    # Generar audio usando OpenAI TTS
                    tts_response = client_openai.audio.speech.create(
                        model="gpt-4o-mini-tts",
                        voice="shimmer",  # Opciones: alloy, echo, fable, onyx, nova, shimmer
                        input=assistant_response,
                        speed=1.25
                    )
                    
                    # Guardar en bytes para reproducir
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
        st.error(f"Error al generar respuesta de DeepSeek: {e}")

st.markdown("---")

# Sidebar con información adicional
with st.sidebar:
    st.subheader("ℹ️ Información")
    st.info("""
    **CETES** son instrumentos de deuda gubernamental 
    de bajo riesgo que ofrecen rendimientos atractivos.
    """)
    
    st.markdown("---")
    st.subheader("📚 Recursos")
    st.markdown("""
    - [Banco de México](https://www.banxico.org.mx)
    - [CETES Directo](https://www.cetesdirecto.com)
    """)
    
