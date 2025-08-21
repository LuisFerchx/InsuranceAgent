import json
import os
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

from app.core.config import get_settings

load_dotenv()


class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            self.model_name,
            generation_config=genai.GenerationConfig(
                temperature=0,
                response_mime_type="application/json"
            )
        )

    def extract_slots(self, user_text: str) -> Dict[str, Any]:
        """Extrae información del texto del usuario usando Gemini"""
        system_prompt = """
Eres un extractor ESTRICTO de datos para pre-cotización vehicular.
Devuelve SIEMPRE JSON con el SIGUIENTE ESQUEMA EXACTO (sin texto adicional):

{
  "vehicle_year": int|null,
  "vehicle_make": string|null,
  "vehicle_model": string|null,
  "vehicle_value_usd": float|null,
  "usage": "particular"|"comercial"|null,
  "city": string|null,
  "driver_age": int|null,
  "claims_last3y": int|null,
  "anti_theft": true|false|null,
  "garage_overnight": true|false|null,
  "deductible_pct": 5|10|15|20|null,
  "addons": ["asistencia_vial"|"auto_reemplazo"|"cobertura_lunas"]|null
}

- Usa null si no estás seguro.
- "vehicle_value_usd" en dólares; si no es claro, null.
- Mapea sinónimos: asistencia_vial~grúa~auxilio; auto_reemplazo~vehículo sustituto; cobertura_lunas~parabrisas~vidrios.
- NO expliques, NO comentes, NO inventes. SOLO JSON.
"""

        examples = [
            ("Kia Rio 2018, uso particular, Guayaquil, vale 12 mil dólares. Conductor 28 años, sin siniestros. Deducible 10%, quiero asistencia vial.",
             {
                "vehicle_year": 2018, "vehicle_make": "Kia", "vehicle_model": "Rio",
                "vehicle_value_usd": 12000.0, "usage": "particular", "city": "Guayaquil",
                "driver_age": 28, "claims_last3y": 0, "anti_theft": None, "garage_overnight": None,
                "deductible_pct": 10, "addons": ["asistencia_vial"]
             }),
            ("Trabajo con una Hilux 2021 en Quito. Vale 28k, tiene alarma y duerme en garaje. Tengo 45 y un choque hace dos años.",
             {
                "vehicle_year": 2021, "vehicle_make": "Toyota", "vehicle_model": "Hilux",
                "vehicle_value_usd": 28000.0, "usage": "comercial", "city": "Quito",
                "driver_age": 45, "claims_last3y": 1, "anti_theft": True, "garage_overnight": True,
                "deductible_pct": None, "addons": None
             })
        ]

        parts = [system_prompt]
        # few-shot examples
        for user_text_example, json_example in examples:
            parts.append(f"Usuario:\n{user_text_example}\n\nJSON:\n{json.dumps(json_example, ensure_ascii=False)}")
        parts.append(f"Usuario:\n{user_text}\n\nJSON:")
        
        try:
            resp = self.model.generate_content(parts)
            text = (resp.text or "").strip()
            return json.loads(text)
        except Exception:
            return {}
