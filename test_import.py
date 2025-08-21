#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación se importe correctamente
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    print("✅ Aplicación importada correctamente")
    print(f"Título: {app.title}")
    print(f"Versión: {app.version}")
    print("✅ Todas las importaciones funcionan correctamente")
except Exception as e:
    print(f"❌ Error al importar la aplicación: {e}")
    import traceback
    traceback.print_exc()
