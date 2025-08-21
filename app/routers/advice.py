from fastapi import APIRouter, Depends
from app.schemas.quote import (
    StartResponse, ReplyRequest, ReplyResponse, QuoteState
)
from app.services.session_service import SessionService
from app.services.gemini_service import GeminiService
from app.services.quote_service import QuoteService
from app.services.question_service import QuestionService
from app.core.config import get_settings

router = APIRouter(prefix="/advice", tags=["advice"])


def get_session_service() -> SessionService:
    """Dependency para obtener el servicio de sesiones"""
    settings = get_settings()
    return SessionService(ttl_seconds=settings.SESSION_TTL_SECONDS)


def get_gemini_service() -> GeminiService:
    """Dependency para obtener el servicio de Gemini"""
    return GeminiService()


@router.post("/start", response_model=StartResponse)
def start(session_service: SessionService = Depends(get_session_service)) -> StartResponse:
    """Inicia una nueva sesión de asesoría"""
    session_service.prune_sessions()
    sid = session_service.new_session_id()
    session_service.create_session(sid, QuoteState())
    
    message = QuestionService.get_welcome_message()
    return StartResponse(session_id=sid, message=message)


@router.post("/reply", response_model=ReplyResponse)
def reply(
    req: ReplyRequest,
    session_service: SessionService = Depends(get_session_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> ReplyResponse:
    print(f"BUENAS NOCHES!!: {session_service.sessions}")
    """Procesa la respuesta del usuario y genera la siguiente pregunta o cotización"""
    session_service.prune_sessions()
    sid = req.session_id
    
    # Verificar si la sesión existe
    if not session_service.session_exists(sid):
        sid = session_service.new_session_id()
        session_service.create_session(sid, QuoteState())
        # return ReplyResponse(
        #     session_id=sid,
        #     message=QuestionService.get_session_expired_message(),
        #     state=QuoteState(),
        #     quote=None
        # )

    # Obtener estado actual
    session_data = session_service.get_session(sid)
    state: QuoteState = session_data["state"]

    # 1) Extraer información con Gemini
    extracted = gemini_service.extract_slots(req.user_text)

    # 2) Mezclar con estado previo (coalesce)
    def coalesce(old, new):
        return new if new not in (None, "", []) else old

    updated = QuoteState(
        vehicle_year=coalesce(state.vehicle_year, extracted.get("vehicle_year")),
        vehicle_make=coalesce(state.vehicle_make, extracted.get("vehicle_make")),
        vehicle_model=coalesce(state.vehicle_model, extracted.get("vehicle_model")),
        vehicle_value_usd=coalesce(state.vehicle_value_usd, extracted.get("vehicle_value_usd")),
        usage=coalesce(state.usage, extracted.get("usage")),
        city=coalesce(state.city, extracted.get("city")),
        driver_age=coalesce(state.driver_age, extracted.get("driver_age")),
        claims_last3y=coalesce(state.claims_last3y, extracted.get("claims_last3y")),
        anti_theft=coalesce(state.anti_theft, extracted.get("anti_theft")),
        garage_overnight=coalesce(state.garage_overnight, extracted.get("garage_overnight")),
        deductible_pct=coalesce(state.deductible_pct, extracted.get("deductible_pct")),
        addons=coalesce(state.addons, extracted.get("addons")),
    )

    # 3) Verificar si faltan campos obligatorios
    missing = updated.missing_fields()
    if missing:
        question = QuestionService.FIELD_QUESTIONS[missing[0]]
        session_service.update_session(sid, updated)
        return ReplyResponse(session_id=sid, message=question, state=updated, quote=None)

    # 4) Verificar preguntas opcionales
    next_q = QuestionService.next_question(updated)
    if next_q:
        session_service.update_session(sid, updated)
        return ReplyResponse(session_id=sid, message=next_q, state=updated, quote=None)

    # 5) Generar cotización completa
    quote_result = QuoteService.generate_quote(updated)
    message = QuestionService.format_quote_message(
        quote_result.offers,
        quote_result.recommendation,
        quote_result.disclaimer
    )

    session_service.update_session(sid, updated)
    return ReplyResponse(session_id=sid, message=message, state=updated, quote=quote_result)
