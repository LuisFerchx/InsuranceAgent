# FastAPI Project

A REST API built with FastAPI that provides intelligent auto insurance advisory with automatic documentation.

## Features

- ✅ FastAPI with automatic documentation (Swagger/OpenAPI)
- ✅ Intelligent auto insurance advisory with AI
- ✅ Session management with automatic TTL
- ✅ Data validation with Pydantic
- ✅ Configuration with environment variables
- ✅ Unit tests
- ✅ Modular and scalable structure
- ✅ CORS configured

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository>
   cd fastapi-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configurations
   ```

## Usage

### Run in development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run in production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run tests
```bash
pytest
```

## Available Endpoints

### Insurance Advisory
- `POST /advice/start` - Start new advisory session
- `POST /advice/reply` - Process user response and generate next question or quote

## Documentation

Once you run the application, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Insurance Advisory APIs

### POST /advice/start

Starts a new advisory session for auto insurance quotes.

**Response:**
```json
{
  "session_id": "uuid-string",
  "message": "Welcome message and first question"
}
```

### POST /advice/reply

Processes the user's response and generates the next question or final quote.

**Request:**
```json
{
  "session_id": "uuid-string",
  "user_text": "User response"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "message": "Next question or quote",
  "state": {
    "vehicle_year": 2020,
    "vehicle_make": "Toyota",
    "vehicle_model": "Corolla",
    "vehicle_value_usd": 25000.0,
    "usage": "personal",
    "city": "Mexico City",
    "driver_age": 30,
    "claims_last3y": 0,
    "anti_theft": true,
    "garage_overnight": true,
    "deductible_pct": 10,
    "addons": ["roadside_assistance", "auto_replacement"]
  },
  "quote": {
    "offers": [
      {
        "carrier": "Insurance ABC",
        "plan": "Medium",
        "annual_premium_usd": 1200.0,
        "deductible_pct": 10,
        "addons": ["roadside_assistance"],
        "coverage_notes": "Complete coverage"
      }
    ],
    "recommendation": "We recommend the Medium plan",
    "disclaimer": "Prices are estimates"
  }
}
```

**Usage flow:**
1. Call `/advice/start` to start session
2. Use the returned `session_id` in subsequent calls to `/advice/reply`
3. Answer the system's questions with vehicle and driver information
4. The system will automatically generate a quote when it has all necessary information

**Required fields for quote:**
- `vehicle_year`: Vehicle year (1980-2035)
- `vehicle_make`: Vehicle brand
- `vehicle_model`: Vehicle model
- `vehicle_value_usd`: Vehicle value in USD
- `usage`: Vehicle usage ("personal" or "commercial")
- `city`: City of residence
- `driver_age`: Driver age (16-90)
- `claims_last3y`: Claims in the last 3 years (0-10)

## Project Structure

```
├── app/
│   ├── core/           # Central configuration
│   ├── routers/        # API endpoints
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business services
│   └── utils/          # Utilities
├── tests/              # Unit tests
├── main.py             # Entry point
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Configuration

The main environment variables are:

- `DEBUG`: Debug mode (True/False)
- `SESSION_TTL_SECONDS`: Session lifetime in seconds (default: 3600)

## Contributing

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is under the MIT License. See the `LICENSE` file for more details.
