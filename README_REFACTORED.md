# Agente de Asesoría y Cotización (Vehículos) - Refactorizado

Este proyecto ha sido refactorizado para seguir una estructura modular y organizada, manteniendo toda la funcionalidad original del archivo `main.py`.

## Estructura del Proyecto

```
agent_insurance/
├── app/                          # Módulo principal de la aplicación
│   ├── __init__.py
│   ├── main.py                   # Aplicación FastAPI principal
│   ├── core/                     # Configuración y utilidades core
│   │   ├── __init__.py
│   │   └── config.py             # Configuración de la aplicación
│   ├── schemas/                  # Modelos de datos Pydantic
│   │   ├── __init__.py
│   │   ├── user.py               # Esquemas de usuario (existente)
│   │   └── quote.py              # Esquemas de cotización (nuevo)
│   ├── services/                 # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── session_service.py    # Gestión de sesiones
│   │   ├── gemini_service.py     # Integración con Gemini AI
│   │   ├── quote_service.py      # Lógica de cotización
│   │   └── question_service.py   # Lógica de preguntas
│   ├── routers/                  # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── health.py             # Endpoint de salud (existente)
│   │   ├── users.py              # Endpoints de usuario (existente)
│   │   └── advice.py             # Endpoints de asesoría (nuevo)
│   ├── models/                   # Modelos de base de datos
│   ├── database/                 # Configuración de BD
│   └── utils/                    # Utilidades
├── main.py                       # Punto de entrada (refactorizado)
├── run.py                        # Script de ejecución
├── requirements.txt
├── .env
└── README.md
```

## Módulos Principales

### 1. Configuración (`app/core/`)
- **config.py**: Configuración centralizada de la aplicación, incluyendo variables de entorno para Gemini API.

### 2. Esquemas (`app/schemas/`)
- **quote.py**: Modelos Pydantic para cotizaciones:
  - `QuoteState`: Estado de la cotización
  - `StartResponse`, `ReplyRequest`, `ReplyResponse`: Endpoints de asesoría
  - `Offer`, `QuoteResult`: Resultados de cotización

### 3. Servicios (`app/services/`)
- **session_service.py**: Gestión de sesiones en memoria con TTL
- **gemini_service.py**: Integración con Google Gemini para extracción de datos
- **quote_service.py**: Lógica de cotización y cálculo de primas
- **question_service.py**: Lógica de preguntas y flujo de conversación

### 4. Routers (`app/routers/`)
- **advice.py**: Endpoints `/advice/start` y `/advice/reply`

## Funcionalidades Mantenidas

✅ **Todas las funcionalidades del archivo original se mantienen:**

- Extracción de datos con Gemini AI
- Gestión de sesiones con TTL
- Lógica de preguntas progresivas
- Cálculo de cotizaciones con múltiples aseguradoras
- Validación de datos con Pydantic
- Endpoints REST completos

## Beneficios de la Refactorización

1. **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad específica
2. **Mantenibilidad**: Código más fácil de mantener y extender
3. **Testabilidad**: Servicios independientes más fáciles de testear
4. **Reutilización**: Servicios pueden ser reutilizados en otros contextos
5. **Configuración Centralizada**: Variables de entorno y configuración en un solo lugar
6. **Dependencias Claras**: Uso de dependency injection de FastAPI

## Cómo Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tu GEMINI_API_KEY

# Ejecutar la aplicación
python run.py
# o
python main.py
```

## Endpoints Disponibles

- `POST /advice/start`: Iniciar nueva sesión de asesoría
- `POST /advice/reply`: Procesar respuesta del usuario
- `GET /health`: Verificar estado de la aplicación

## Migración desde el Código Original

El archivo `main.py` original ha sido completamente refactorizado en módulos separados, pero mantiene exactamente la misma funcionalidad. Los cambios principales son:

1. **Organización**: Código distribuido en módulos lógicos
2. **Dependency Injection**: Uso de FastAPI Depends para servicios
3. **Configuración**: Variables de entorno centralizadas
4. **Estructura**: Seguimiento de mejores prácticas de FastAPI

La aplicación sigue siendo compatible con el código original y puede ejecutarse de la misma manera.
