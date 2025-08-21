"""
Punto de entrada principal de la aplicación.
Importa la aplicación FastAPI desde el módulo app.
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import get_settings
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
