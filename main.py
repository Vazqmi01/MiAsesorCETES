import streamlit as st
import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Mi Asesor CETES",
    page_icon="💰",
    layout="wide"
)

# --- Interfaz de Usuario (UI) de Streamlit ---

# Logo y Título
col1, col2, col3 = st.columns([1, 2, 1])

st.title("Mi Asesor CETES")
st.subheader("Invierte con Inteligencia: Tu herramienta de pronóstico de CETES")
st.markdown("---")

# Contenido principal
st.write("Bienvenido a Mi Asesor CETES. Esta aplicación te ayudará a realizar pronósticos de CETES.")

# Ejemplo de contenido
st.header("Información")
st.info("Esta es una aplicación básica de Streamlit. Puedes comenzar a agregar funcionalidades aquí.")

# Sidebar
with st.sidebar:
    st.header("Configuración")
    st.write("Aquí puedes agregar controles y opciones")

if __name__ == "__main__":
    pass
