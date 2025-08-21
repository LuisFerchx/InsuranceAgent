#!/usr/bin/env python3
"""
Script de debug para verificar las importaciones paso a paso
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Verificando importaciones paso a paso...")

try:
    print("1. Importando configuración...")
    from app.core.config import get_settings
    settings = get_settings()
    print(f"   ✅ Configuración cargada: {settings.PROJECT_NAME}")
    print(f"   ✅ GEMINI_API_KEY configurada: {'Sí' if settings.GEMINI_API_KEY else 'No'}")
except Exception as e:
    print(f"   ❌ Error en configuración: {e}")
    sys.exit(1)

try:
    print("2. Importando esquemas...")
    from app.schemas.quote import QuoteState, StartResponse, ReplyRequest
    print("   ✅ Esquemas importados correctamente")
except Exception as e:
    print(f"   ❌ Error en esquemas: {e}")
    sys.exit(1)

try:
    print("3. Importando servicios...")
    from app.services.session_service import SessionService
    from app.services.gemini_service import GeminiService
    from app.services.quote_service import QuoteService
    from app.services.question_service import QuestionService
    print("   ✅ Servicios importados correctamente")
except Exception as e:
    print(f"   ❌ Error en servicios: {e}")
    sys.exit(1)

try:
    print("4. Importando routers...")
    from app.routers.advice import router as advice_router
    from app.routers.health import router as health_router
    print("   ✅ Routers importados correctamente")
except Exception as e:
    print(f"   ❌ Error en routers: {e}")
    sys.exit(1)

try:
    print("5. Importando aplicación principal...")
    from app.main import app
    print(f"   ✅ Aplicación importada: {app.title}")
    print("   ✅ Todas las importaciones funcionan correctamente")
except Exception as e:
    print(f"   ❌ Error en aplicación principal: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
