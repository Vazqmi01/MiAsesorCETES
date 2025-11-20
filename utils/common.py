import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import base64
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

# Carga de variables de entorno
load_dotenv(override=True)

# Claves API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
BANXICO_API_KEY = os.getenv("BANXICO_API_KEY")
BANXICO_API = os.getenv("BANXICO_API")  # También soportar BANXICO_API

# Inicializar clientes
client_openai = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
client_deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL) if DEEPSEEK_API_KEY else None
client_banxico = OpenAI(api_key=BANXICO_API_KEY)  if BANXICO_API_KEY else None


model_deepseek = "deepseek-chat"

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
        audio.addEventListener('loadedmetadata', function() {{
            audio.playbackRate = {playback_speed};
        }});
    </script>
    """
    return audio_html

def descarga_bmx_series(series_dict, fechainicio, fechafin):
    """
    Descarga series de datos económicos del API de Banxico.
    Args:
        series_dict (dict): Diccionario con el ID de la serie como clave 
                            y el nombre deseado de la columna como valor.
        fechainicio (str): Fecha de inicio de la descarga (YYYY-MM-DD).
        fechafin (str): Fecha de fin de la descarga (YYYY-MM-DD).
    Returns:
        pd.DataFrame or None: DataFrame con todas las series concatenadas,
                              o None si no se descargaron datos.
    """
    # Usar BANXICO_API_KEY
    token = BANXICO_API_KEY
    
    if not token:
        print("Error: La variable de entorno 'BANXICO_API' o 'BANXICO_API_KEY' no está configurada.")
        return None
        
    headers = {'Bmx-Token': token}
    all_data = []
    for serie, nombre in series_dict.items():
        # Construye la URL para la consulta API
        url = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}/datos/{fechainicio}/{fechafin}/'
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f'Error en la consulta para la serie **{nombre}** ({serie}), código **{response.status_code}**')
                continue
            raw_data = response.json()
            # Verifica la estructura del JSON y si contiene datos
            if 'bmx' in raw_data and 'series' in raw_data['bmx'] and len(raw_data['bmx']['series']) > 0:
                serie_data = raw_data['bmx']['series'][0]
                if 'datos' in serie_data and len(serie_data['datos']) > 0:
                    data = serie_data['datos']
                    df = pd.DataFrame(data)
                    
                    # Procesa y limpia los datos
                    df['dato'] = df['dato'].replace('N/E', np.nan).astype(float)
                    # La fecha de Banxico a menudo tiene formato 'DD/MM/YYYY'
                    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True, errors='coerce') 
                    
                    # Elimina filas con fecha no válida antes de establecer el índice
                    df.dropna(subset=['fecha'], inplace=True)
                    
                    df.set_index('fecha', inplace=True)
                    df.rename(columns={'dato': nombre}, inplace=True)
                    
                    # Solo mantiene la columna con el nombre de la serie
                    all_data.append(df[[nombre]]) 
                else:
                    print(f"No se encontraron datos en el campo 'datos' para la serie **{nombre}** ({serie})")
            else:
                print(f"Estructura inesperada o datos faltantes para la serie **{nombre}** ({serie})")
                
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión o petición para la serie **{nombre}** ({serie}): {e}")
            continue
    # Concatena todos los DataFrames
    if all_data:
        # Usa join='outer' para asegurar que todas las fechas estén presentes
        df_final = pd.concat(all_data, axis=1, join='outer') 
        return df_final
    else:
        print("No se descargaron datos.")
        return None

def obtener_datos_banxico(fechainicio='2006-01-01', fechafin=None):
    """
    Obtiene y procesa datos de Banxico para CETES y otras series económicas.
    Args:
        fechainicio (str): Fecha de inicio (YYYY-MM-DD). Por defecto '2006-01-01'.
        fechafin (str): Fecha de fin (YYYY-MM-DD). Si es None, usa la fecha actual.
    Returns:
        pd.DataFrame or None: DataFrame procesado con datos semanales, o None si hay error.
    """
    if fechafin is None:
        fechafin = datetime.now().strftime('%Y-%m-%d')
    
    # Definición de las series de Banxico a descargar
    series = {
        'SF43936': 'CETE_28D',
        'SF43939': 'CETE_91D',
        'SF43942': 'CETE_182D',
        'SF43945': 'CETE_364D',
        'SF61745': 'Tasa_Objetivo',
        'SI237': 'Tasa_FED',
        'SF43718': 'Tipo_Cambio_Fix',
        'SP1': 'INPC'
    }
    
    df_final = descarga_bmx_series(series, fechainicio, fechafin)
    
    if df_final is None:
        return None
    
    # Ordena el índice por fecha
    df_final.sort_index(inplace=True)
    
    # Relleno de Datos Faltantes (ffill)
    columns_to_ffill = ['CETE_28D','CETE_91D','CETE_182D','CETE_364D', 'Tasa_Objetivo', 'INPC', 'Tasa_FED', 'Tipo_Cambio_Fix']
    for col in columns_to_ffill:
        if col in df_final.columns:
            df_final[col] = df_final[col].ffill()
    
    # Creación del DataFrame Maestro con Frecuencia Semanal
    if 'CETE_28D' in df_final.columns:
        cetes_28d_series = df_final['CETE_28D'].dropna()
        
        if not cetes_28d_series.empty:
            # Crea un índice semanal (jueves) desde la primera hasta la última fecha de CETE_28D
            idx = pd.date_range(start=cetes_28d_series.index.min(), 
                                end=cetes_28d_series.index.max(), 
                                freq='W-THU')
            
            df_master = pd.DataFrame(index=idx)
            
            # Combina el índice semanal con los datos descargados
            df = pd.merge(df_master, df_final, left_index=True, right_index=True, how='left')
            
            # Asegura que las columnas rellenadas anteriormente se mantengan rellenadas
            for col in columns_to_ffill:
                if col in df.columns:
                    df[col] = df[col].ffill()
            
            return df
        else:
            print("No hay datos válidos en la serie 'CETE_28D' para crear el índice semanal.")
            return None
    else:
        print("La serie 'CETE_28D' no se descargó correctamente para crear el índice semanal.")
        return None

def pronostico_sarimax(df, variable_objetivo, exog_cols, periodos_pronostico=30, 
                       order=(1, 1, 1), seasonal_order=(1, 1, 1, 52)):
    """
    Genera pronósticos usando el modelo SARIMAX con variables exógenas.
    
    Args:
        df (pd.DataFrame): DataFrame con datos históricos (índice debe ser fecha)
        variable_objetivo (str): Nombre de la columna a predecir (debe estar en cetes_cols)
        exog_cols (list): Lista de columnas exógenas (variables predictoras)
        periodos_pronostico (int): Número de períodos a pronosticar
        order (tuple): Parámetros (p, d, q) del modelo ARIMA. Default: (1, 1, 1)
        seasonal_order (tuple): Parámetros estacionales (P, D, Q, s). Default: (1, 1, 1, 52) para datos semanales
    
    Returns:
        tuple: (pronostico, fechas_pronostico, modelo_ajustado)
            - pronostico: Serie con los valores pronosticados
            - fechas_pronostico: Índice de fechas para el pronóstico
            - modelo_ajustado: Modelo SARIMAX ajustado
    """
    try:
        # Preparar datos
        df_work = df.copy()
        
        # Verificar que la variable objetivo existe
        if variable_objetivo not in df_work.columns:
            raise ValueError(f"La variable objetivo '{variable_objetivo}' no existe en el DataFrame")
        
        # Filtrar datos válidos (sin NaN en la variable objetivo)
        df_work = df_work.dropna(subset=[variable_objetivo])
        
        if len(df_work) < 52:  # Necesitamos al menos un año de datos semanales
            raise ValueError(f"Se necesitan al menos 52 observaciones. Solo hay {len(df_work)}")
        
        # Separar variable endógena y exógenas
        y = df_work[variable_objetivo]
        
        # Preparar variables exógenas (solo las que existen y tienen datos)
        exog_train = None
        exog_cols_validas = []
        
        for col in exog_cols:
            if col in df_work.columns and col != variable_objetivo:
                # Rellenar NaN con forward fill
                exog_series = df_work[col].ffill().bfill()
                if not exog_series.isna().all():
                    exog_cols_validas.append(col)
        
        # Crear DataFrame de exógenas si hay variables disponibles
        if exog_cols_validas:
            exog_train = df_work[exog_cols_validas].copy()
            # Asegurar que tenga el mismo índice que y y rellenar NaN
            exog_train = exog_train.reindex(y.index)
            exog_train = exog_train.ffill().bfill()
        
        # Ajustar modelo SARIMAX
        if exog_train is not None and not exog_train.empty:
            modelo = SARIMAX(
                y,
                exog=exog_train,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
        else:
            # Si no hay exógenas, usar SARIMA simple
            modelo = SARIMAX(
                y,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
        
        modelo_ajustado = modelo.fit(disp=False, maxiter=50)
        
        # Generar pronóstico
        fecha_fin = y.index[-1]
        
        # Crear fechas futuras (asumiendo frecuencia semanal)
        if isinstance(y.index, pd.DatetimeIndex):
            freq = pd.infer_freq(y.index)
            if freq is None:
                # Si no se puede inferir, usar frecuencia semanal por defecto
                freq = 'W-THU'
        else:
            freq = 'W-THU'
        
        fechas_pronostico = pd.date_range(
            start=fecha_fin + timedelta(weeks=1),
            periods=periodos_pronostico,
            freq=freq
        )
        
        # Preparar exógenas para el pronóstico
        # Para el pronóstico, usamos el último valor conocido de cada variable exógena
        # En producción, podrías usar pronósticos de las variables exógenas también
        if exog_train is not None and not exog_train.empty:
            # Usar el último valor de cada variable exógena para todo el horizonte de pronóstico
            exog_forecast = pd.DataFrame(
                index=fechas_pronostico,
                columns=exog_train.columns
            )
            for col in exog_train.columns:
                # Usar el último valor conocido
                exog_forecast[col] = exog_train[col].iloc[-1]
            
            pronostico = modelo_ajustado.forecast(steps=periodos_pronostico, exog=exog_forecast)
        else:
            pronostico = modelo_ajustado.forecast(steps=periodos_pronostico)
        
        # Crear serie con índice de fechas
        pronostico_series = pd.Series(pronostico, index=fechas_pronostico)
        
        return pronostico_series, fechas_pronostico, modelo_ajustado
        
    except Exception as e:
        raise Exception(f"Error al generar pronóstico SARIMAX: {str(e)}")
