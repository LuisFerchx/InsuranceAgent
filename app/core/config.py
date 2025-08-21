from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Configuración básica
    PROJECT_NAME: str = "Agente de Asesoría y Cotización (Vehículos) - Gemini"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para asesoría y cotización de seguros vehiculares usando Gemini"
    API_V1_STR: str = "/api/v1"
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu-clave-secreta-aqui")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Configuración de CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración de Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Configuración de sesiones
    SESSION_TTL_SECONDS: int = 60 * 60  # 1 hora
    
    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()

settings = get_settings()
