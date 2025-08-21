# FastAPI Project

Una API REST construida con FastAPI que incluye autenticación, gestión de usuarios y documentación automática.

## Características

- ✅ FastAPI con documentación automática (Swagger/OpenAPI)
- ✅ Autenticación JWT
- ✅ Gestión de usuarios (CRUD)
- ✅ Validación de datos con Pydantic
- ✅ Configuración con variables de entorno
- ✅ Tests unitarios
- ✅ Estructura modular y escalable
- ✅ CORS configurado
- ✅ Health checks

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd fastapi-project
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

## Uso

### Ejecutar en desarrollo
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar en producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Ejecutar tests
```bash
pytest
```

## Endpoints disponibles

### Health Checks
- `GET /api/v1/health` - Health check básico
- `GET /api/v1/health/detailed` - Health check detallado

### Usuarios
- `GET /api/v1/users/` - Listar usuarios
- `GET /api/v1/users/{user_id}` - Obtener usuario específico
- `POST /api/v1/users/` - Crear usuario
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario

## Documentación

Una vez que ejecutes la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Estructura del proyecto

```
├── app/
│   ├── core/           # Configuración central
│   ├── database/       # Configuración de base de datos
│   ├── models/         # Modelos SQLAlchemy
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Esquemas Pydantic
│   └── utils/          # Utilidades
├── tests/              # Tests unitarios
├── main.py             # Punto de entrada
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## Configuración

Las variables de entorno principales son:

- `SECRET_KEY`: Clave secreta para JWT
- `DATABASE_URL`: URL de conexión a la base de datos
- `DEBUG`: Modo debug (True/False)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
