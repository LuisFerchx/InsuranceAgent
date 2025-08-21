from typing import List
from app.schemas.quote import QuoteState


class QuestionService:
    """Servicio para manejar la lógica de preguntas y completar información faltante"""

    FIELD_QUESTIONS = {
        "vehicle_year": "¿De qué año es tu vehículo?",
        "vehicle_make": "¿Cuál es la **marca** del vehículo? (ej., Chevrolet, Kia, Toyota)",
        "vehicle_model": "¿Cuál es el **modelo**? (ej., Sail, Rio, Hilux)",
        "vehicle_value_usd": "¿Cuál es el **valor referencial** del vehículo en USD?",
        "usage": "¿El uso es **particular** o **comercial**?",
        "city": "¿En qué **ciudad** circula principalmente el vehículo?",
        "driver_age": "¿Qué **edad** tiene el conductor principal?",
        "claims_last3y": "¿Cuántos **siniestros** tuviste en los últimos 3 años?",
    }

    OPTIONAL_QUESTIONS = {
        "anti_theft": "¿Tiene **alarma/antirrobo**? (sí/no)",
        "garage_overnight": "¿Duerme en **garaje** por las noches? (sí/no)",
        "deductible_pct": "¿Qué **deducible** prefieres? (5%, 10%, 15% o 20%)",
        "addons": "¿Deseas **asistencia vial**, **auto de reemplazo** o **cobertura de lunas**? (puedes decir 'ninguno')",
    }

    @staticmethod
    def next_question(state: QuoteState) -> str:
        """Determina la siguiente pregunta basada en el estado actual"""
        missing = state.missing_fields()
        if missing:
            return QuestionService.FIELD_QUESTIONS[missing[0]]
        
        for field, question in QuestionService.OPTIONAL_QUESTIONS.items():
            if getattr(state, field) is None:
                return question
        
        return ""

    @staticmethod
    def get_welcome_message() -> str:
        """Retorna el mensaje de bienvenida"""
        return (
            "¡Hola! Soy tu asesor virtual de seguros vehiculares.\n\n"
            "Para cotizar opciones directo con aseguradoras necesito:\n"
            "• Año, marca y modelo • Valor (USD) • Uso (particular/comercial)\n"
            "• Ciudad principal • Edad del conductor • Siniestros últimos 3 años\n\n"
            "Cuéntame lo que tengas y te pido solo lo que falte."
        )

    @staticmethod
    def get_session_expired_message() -> str:
        """Retorna el mensaje cuando la sesión ha expirado"""
        return "La sesión previa caducó. Empecemos de nuevo, ¿qué datos del vehículo tienes?"

    @staticmethod
    def format_quote_message(offers: List, recommendation: str, disclaimer: str) -> str:
        """Formatea el mensaje de cotización"""
        return (
            f"Estas son tus mejores opciones (anual, USD):\n"
            f"1) {offers[0].carrier} - {offers[0].plan}: {offers[0].annual_premium_usd}\n"
            f"2) {offers[1].carrier} - {offers[1].plan}: {offers[1].annual_premium_usd}\n"
            f"3) {offers[2].carrier} - {offers[2].plan}: {offers[2].annual_premium_usd}\n\n"
            f"{recommendation}\n\n{disclaimer}"
        )
