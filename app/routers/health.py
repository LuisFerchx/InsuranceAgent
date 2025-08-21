from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Endpoint para verificar el estado de salud de la API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FastAPI"
    }

@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Endpoint para verificar el estado detallado de la API
    """
    try:
        # Aquí puedes agregar verificaciones adicionales
        # como conexión a base de datos, servicios externos, etc.
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "FastAPI",
            "version": "1.0.0",
            "checks": {
                "database": "ok",
                "external_services": "ok"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
