import streamlit as st
import requests
from io import BytesIO
from gtts import gTTS

# --- Configuración segura ---
st.set_page_config(
    page_title="Tutor de Inglés Seguro",
    page_icon="🔒",
    layout="wide"
)

# --- Diseño estilo Duolingo ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #58cc02;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background: white !important;
        color: #58cc02 !important;
        border-radius: 12px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Carga el token desde Secrets ---
try:
    HF_KEY = st.secrets["HUGGINGFACE_KEY"]
except:
    st.error("🔐 Configura tu API Key en Secrets")
    st.stop()

# --- Funciones principales ---
def transcribir_audio(audio_bytes):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    
    try:
        response = requests.post(API_URL, headers=headers, data=audio_bytes.getvalue())
        return response.json().get("text", "No pude entender el audio")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return ""

def generar_respuesta(texto):
    respuesta_ia = f"¡Bien dicho! Practiquemos: '{texto}'. Ahora di: 'How are you today?'"
    
    # Audio en memoria (sin guardar archivos)
    audio_io = BytesIO()
    tts = gTTS(text=respuesta_ia, lang="en")
    tts.write_to_fp(audio_io)
    return respuesta_ia, audio_io

# --- Interfaz ---
st.title("🌍 Tutor de Inglés Seguro")
audio_file = st.file_uploader("Sube tu audio en inglés (.wav)", type=["wav"])

if audio_file:
    if st.button("📝 Analizar"):
        with st.spinner("Procesando..."):
            texto = transcribir_audio(audio_file)
            
            if texto:
                st.success(f"🎤 Tú: {texto}")
                respuesta, audio = generar_respuesta(texto)
                st.info(f"👩🏫 IA: {respuesta}")
                st.audio(audio.getvalue(), format="audio/mp3")