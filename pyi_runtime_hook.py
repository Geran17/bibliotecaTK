"""
Runtime hook para PyInstaller - Ajusta el path de búsqueda de módulos
"""

import sys
import os

# Obtener la ruta del ejecutable
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # Estamos en un ejecutable de PyInstaller
    base_dir = sys._MEIPASS
else:
    # Estamos en desarrollo
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Agregar la ruta base al path de Python para que pueda encontrar los módulos
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
