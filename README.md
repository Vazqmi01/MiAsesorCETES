# �� Mi Asesor CETES

Aplicación web inteligente desarrollada con Streamlit para realizar pronósticos y análisis de los Certificados de la Tesorería de la Federación (CETES). Incluye un asistente experto con inteligencia artificial que te ayuda a entender y analizar las tasas de CETES.

## ✨ Características Principales

- 📊 **Análisis y Pronósticos**: Genera pronósticos de tasas de CETES usando modelos SARIMAX para plazos de 28, 91, 182 y 364 días
- 🤖 **Asesor Experto con IA**: Chatbot inteligente que responde preguntas sobre CETES, Banxico, inflación e inversiones (usa OpenAI GPT)
- 🎤 **Entrada por Voz**: Transcribe preguntas habladas y reproduce respuestas con síntesis de voz
- 📈 **Gráficas Interactivas**: Visualiza tendencias históricas y pronósticos con gráficas interactivas de Plotly
- 📉 **Estadísticas**: Análisis estadístico de los datos históricos de CETES
- 🔄 **Actualización Automática**: Obtiene datos actualizados directamente de la API de Banxico

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de OpenAI (para el asesor experto con IA y transcripción/síntesis de voz)
- **Acceso a la API de Banxico (requerido)**

## 🚀 Instalación

### 1. Clonar el repositorio (si aplica)

```bash
git clone <url-del-repositorio>
cd MiAsesorCETES
```

### 2. Crear un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

# API de OpenAI (requerido para el asesor experto)
OPENAI_API_KEY=tu_clave_api_openai

# API de Banxico (requerido)
BANXICO_API_KEY=tu_clave_api_banxico**Importante**: La aplicación **requiere** una clave válida de la API de Banxico para funcionar correctamente. Sin esta clave, no podrás acceder a los datos históricos ni generar pronósticos.

### Cómo obtener las claves de API

- **OpenAI**: Regístrate en [OpenAI](https://platform.openai.com/) y genera una API key
- **Banxico**: Consulta la [documentación de la API de Banxico](https://www.banxico.org.mx/SieAPIRest/service/v1/) para obtener tu clave

## 🏃 Ejecución

### Opción 1: Usando el script (Recomendado)

```bash
chmod +x run.sh  # Solo la primera vez
./run.sh
```

El script automáticamente:
- Crea el entorno virtual si no existe
- Instala las dependencias
- Ejecuta la aplicación

### Opción 2: Ejecución manual

1. Activa el entorno virtual:
source venv/bin/activate  # En Windows: venv\Scripts\activate2. Ejecuta Streamlit:
streamlit run main.pyLa aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Uso de la Aplicación

### Página Principal (🏡 Bienvenido)
- Presentación general de la aplicación
- Información sobre las características disponibles

### Página 1: 📊 Asesor Experto
- Chatea con un experto en CETES usando inteligencia artificial
- Haz preguntas por texto o voz sobre:
  - Qué son los CETES y cómo funcionan
  - Tasas de interés y plazos
  - Relación con la inflación (INPC)
  - Comparativas con otros instrumentos financieros
  - Pronósticos y tendencias
- El asistente tiene acceso a pronósticos actualizados generados por modelos SARIMAX

### Página 2: 📈 Pronósticos y Gráficas
- **Pestaña "Gráficas y Pronósticos"**:
  - Visualiza tendencias históricas de CETES
  - Muestra pronósticos para los próximos días
  - Compara diferentes plazos de CETES
  
- **Pestaña "Estadísticas"**:
  - Estadísticas descriptivas de las tasas
  - Análisis de volatilidad
  - Correlaciones entre plazos
  
- **Pestaña "Datos"**:
  - Tabla completa de datos históricos
  - Datos de pronósticos generados
  - Exportación de datos

## 📁 Estructura del Proyecto

```
MiAsesorCETES/
├── main.py                          # Archivo principal de la aplicación
├── prompts.py                       # Prompts del sistema para el asesor experto
├── requirements.txt                 # Dependencias del proyecto
├── run.sh                           # Script para ejecutar la aplicación
├── .env                             # Variables de entorno (crear manualmente)
├── README.md                        # Este archivo
├── pages/                           # Páginas de la aplicación Streamlit
│   ├── 1_📊_Asesor_Experto.py      # Página del asesor experto con IA
│   └── 2_📈_Pronosticos_y_Graficas.py  # Página de gráficas y pronósticos
├── utils/                           # Utilidades
│   ├── __init__.py
│   └── common.py                    # Funciones comunes (obtención de datos, pronósticos, etc.)
└── images/                          # Imágenes de la aplicación
    ├── Logo.png
    └── README.md
```

## 🔧 Dependencias Principales

- **streamlit**: Framework para la aplicación web
- **pandas**: Manipulación y análisis de datos
- **plotly**: Gráficas interactivas
- **statsmodels**: Modelos estadísticos (SARIMAX para pronósticos)
- **openai**: Cliente para la API de OpenAI (GPT, transcripción de voz y síntesis de voz)
- **requests**: Solicitudes HTTP a la API de Banxico
- **python-dotenv**: Carga de variables de entorno
- **streamlit-audiorecorder**: Grabación de audio en Streamlit

## 🎯 Características Técnicas

- **Modelos de Pronóstico**: SARIMAX para series temporales
- **Fuente de Datos**: API de Banxico
- **IA del Asesor**: OpenAI GPT con contexto especializado en CETES
- **Transcripción de Voz**: API de Transcripción de OpenAI (gpt-4o-mini-transcribe)
- **Síntesis de Voz**: OpenAI TTS
- **Visualización**: Plotly para gráficas interactivas

## ⚠️ Notas Importantes

- **Propósito Educativo**: Esta aplicación tiene fines educativos e informativos.
- **Datos Históricos**: Los datos se obtienen directamente de la API de Banxico. Se requiere una clave válida de API para funcionar.
- **Pronósticos**: Los pronósticos generados son estimaciones estadísticas y no garantizan resultados futuros.
- **Costo de API**: El uso de OpenAI puede generar costos según tu plan. Consulta los precios en su sitio web.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Ver el archivo `LICENSE` para más detalles.

## 💡 Soporte

Si encuentras algún problema o tienes preguntas, por favor abre un issue en el repositorio del proyecto.

---

**Desarrollado con ❤️ para ayudar a entender y analizar los CETES de manera inteligente.**
