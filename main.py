import streamlit as st
import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
from datetime import datetime
import os
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Mi Asesor CETES",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Funciones auxiliares para imágenes ---
def load_image_from_url(url):
    """Carga una imagen desde una URL"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.content
    except:
        return None
    return None

def get_image_path(filename):
    """Obtiene la ruta de una imagen local"""
    image_dir = Path("images")
    if image_dir.exists():
        image_path = image_dir / filename
        if image_path.exists():
            return str(image_path)
    return None


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
    investment_image = get_image_path("Logo.png")
    if investment_image:
        st.image(investment_image, width=250) 
    else:
        try:
            # También cambiar la imagen de respaldo
            st.image(IMAGES["investment"], width=250) 
        except:
            st.info("💼 Inversiones inteligentes")

st.markdown("---")

# Sección de características con imágenes
st.header("📌 Características Principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Análisis de Datos")
    growth_img = get_image_path("growth.jpg")
    if growth_img:
        st.image(growth_img, use_container_width=True)
    else:
        try:
            st.image(IMAGES["growth"], use_container_width=True)
        except:
            st.info("📈 Crecimiento sostenido")
    st.write("Analiza las tendencias históricas de los CETES con gráficos interactivos y visualizaciones avanzadas.")

with col2:
    st.markdown("### 🧮 Pronósticos")
    calc_img = get_image_path("calculator.jpg") 
    if calc_img:
        st.image(calc_img, use_container_width=True)
    else:
        try:
            st.image(IMAGES["calculator"], use_container_width=True)
        except:
            st.info("🧮 Cálculos precisos")
    st.write("Utiliza modelos para realizar pronósticos precisos de las tasas de interés futuras.")

with col3:
    st.markdown("### 💡 Decisiones Inteligentes")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;'>
        <h2>💡</h2>
        <p>Toma decisiones de inversión basadas en datos y análisis estadístico confiable.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("Obtén recomendaciones personalizadas para optimizar tus inversiones en CETES.")

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
    
if __name__ == "__main__":
    pass
