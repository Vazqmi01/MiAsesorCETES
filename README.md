# Mi Asesor CETES

Aplicación web desarrollada con Streamlit para pronósticos y análisis de CETES.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Crea un entorno virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

### Opción 1: Usando el script (Recomendado)
```bash
./run.sh
```

### Opción 2: Manualmente

1. Activa el entorno virtual:
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Ejecuta Streamlit:
```bash
streamlit run main.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

**Nota:** Asegúrate de activar el entorno virtual antes de ejecutar streamlit, ya que las dependencias están instaladas dentro del entorno virtual.

## Estructura del Proyecto

- `main.py`: Archivo principal de la aplicación Streamlit
- `requirements.txt`: Dependencias del proyecto
- `README.md`: Documentación del proyecto

## Desarrollo

Para desarrollar nuevas funcionalidades, edita el archivo `main.py` y la aplicación se recargará automáticamente.
