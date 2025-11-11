#!/usr/bin/env python3
"""
Script para descargar imágenes de ejemplo para la aplicación Mi Asesor CETES.
Este script descarga imágenes relacionadas con finanzas e inversiones desde Unsplash.
"""

import requests
import os
from pathlib import Path

# Crear carpeta de imágenes si no existe
images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

# URLs de imágenes desde Unsplash (imágenes de alta calidad y gratuitas)
IMAGE_URLS = {
    "hero.jpg": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200&h=400&fit=crop&q=80",
    "investment.jpg": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop&q=80",
    "growth.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop&q=80",
    "calculator.jpg": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&h=600&fit=crop&q=80"
}

def download_image(url, filepath):
    """Descarga una imagen desde una URL y la guarda en el archivo especificado"""
    try:
        print(f"Descargando {filepath.name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ {filepath.name} descargado exitosamente")
        return True
    except Exception as e:
        print(f"✗ Error al descargar {filepath.name}: {e}")
        return False

def main():
    """Función principal para descargar todas las imágenes"""
    print("=" * 50)
    print("Descargando imágenes para Mi Asesor CETES")
    print("=" * 50)
    print()
    
    downloaded = 0
    skipped = 0
    
    for filename, url in IMAGE_URLS.items():
        filepath = images_dir / filename
        
        # Verificar si la imagen ya existe
        if filepath.exists():
            print(f"⊘ {filename} ya existe, omitiendo...")
            skipped += 1
            continue
        
        # Descargar la imagen
        if download_image(url, filepath):
            downloaded += 1
        print()
    
    print("=" * 50)
    print(f"Descarga completada: {downloaded} nuevas, {skipped} omitidas")
    print("=" * 50)
    print()
    print("Las imágenes están listas para usar en la aplicación.")
    print("Ejecuta 'streamlit run main.py' para ver las imágenes en la aplicación.")

if __name__ == "__main__":
    main()

