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

## Imágenes

La aplicación incluye soporte para imágenes relacionadas con finanzas e inversiones.

### Descargar Imágenes de Ejemplo

Para descargar imágenes de ejemplo automáticamente:

```bash
source venv/bin/activate
python download_images.py
```

Esto descargará imágenes desde Unsplash y las guardará en la carpeta `images/`.

### Agregar tus Propias Imágenes

1. Coloca tus imágenes en la carpeta `images/`
2. Nombra las imágenes según estos nombres:
   - `hero.jpg` o `hero.png` - Imagen principal del banner
   - `investment.jpg` o `investment.png` - Imagen de inversiones
   - `growth.jpg` o `growth.png` - Imagen de crecimiento
   - `calculator.jpg` o `calculator.png` - Imagen de calculadora

3. La aplicación cargará automáticamente las imágenes locales si existen
4. Si no hay imágenes locales, se usarán imágenes desde URLs públicas

Ver `images/README.md` para más información.

## Estructura del Proyecto

```
MiAsesorCETES/
├── main.py                 # Archivo principal de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── download_images.py      # Script para descargar imágenes
├── run.sh                  # Script para ejecutar la aplicación
├── README.md               # Este archivo
├── images/                 # Carpeta para imágenes
│   └── README.md          # Documentación de imágenes
└── venv/                   # Entorno virtual (no incluir en git)
```

## Desarrollo

Para desarrollar nuevas funcionalidades, edita el archivo `main.py` y la aplicación se recargará automáticamente.

### Características Actuales

- ✅ Interfaz moderna con imágenes
- ✅ Secciones informativas sobre CETES
- ✅ Sidebar con recursos y configuración
- ✅ Soporte para imágenes locales y desde URLs
- ✅ Diseño responsive y atractivo
