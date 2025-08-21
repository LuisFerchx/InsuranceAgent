from typing import List, Optional, Literal
from app.schemas.quote import QuoteState, Offer, QuoteResult


class QuoteService:
    """Servicio para generar cotizaciones de seguros vehiculares"""

    @staticmethod
    def location_factor(city: str) -> float:
        """Factor de ubicación geográfica"""
        c = (city or "").lower()
        if "guayaquil" in c: return 1.12
        if "quito" in c: return 1.10
        if "cuenca" in c: return 1.02
        return 0.98

    @staticmethod
    def age_factor(age: int) -> float:
        """Factor por edad del conductor"""
        if age < 25: return 1.20
        if age > 60: return 1.10
        return 1.00

    @staticmethod
    def claims_factor(n: int) -> float:
        """Factor por siniestros previos"""
        if n == 0: return 0.90
        if n == 1: return 1.10
        return 1.25

    @staticmethod
    def security_factor(anti: Optional[bool], garage: Optional[bool]) -> float:
        """Factor por medidas de seguridad"""
        f = 1.0
        if anti: f *= 0.95
        if garage: f *= 0.95
        return f

    @staticmethod
    def deductible_factor(pct: Optional[int]) -> float:
        """Factor por deducible"""
        if pct is None or pct == 10: return 1.00
        if pct == 5: return 1.10
        if pct == 15: return 0.95
        if pct == 20: return 0.90
        return 1.00

    @staticmethod
    def base_rate(usage: str) -> float:
        """Tasa base según uso"""
        return 0.025 if usage == "particular" else 0.032

    @staticmethod
    def plan_for_value(value: float) -> Literal["Básica","Media","Full"]:
        """Determina el plan según el valor del vehículo"""
        if value < 12000: return "Básica"
        if value < 25000: return "Media"
        return "Full"

    @staticmethod
    def addons_cost(addons: Optional[List[str]]) -> float:
        """Calcula el costo de add-ons"""
        if not addons: return 0.0
        cost = 0.0
        for a in addons:
            if a == "asistencia_vial": cost += 20
            elif a == "auto_reemplazo": cost += 35
            elif a == "cobertura_lunas": cost += 15
        return cost

    @staticmethod
    def price_formula(state: QuoteState, carrier_bias: float) -> float:
        """Fórmula de cálculo de prima estimada NO vinculante"""
        pure = float(state.vehicle_value_usd) * QuoteService.base_rate(state.usage)
        factors = (
            QuoteService.location_factor(state.city or "") *
            QuoteService.age_factor(int(state.driver_age)) *
            QuoteService.claims_factor(int(state.claims_last3y)) *
            QuoteService.security_factor(state.anti_theft, state.garage_overnight) *
            QuoteService.deductible_factor(state.deductible_pct)
        )
        return round((pure * factors * carrier_bias) + QuoteService.addons_cost(state.addons), 2)

    @staticmethod
    def carrier_andes(state: QuoteState) -> Offer:
        """Cotización de Aseguradora Andes"""
        premium = QuoteService.price_formula(state, carrier_bias=0.98)
        return Offer(
            carrier="Aseguradora Andes",
            plan=QuoteService.plan_for_value(state.vehicle_value_usd or 0),
            annual_premium_usd=premium,
            deductible_pct=state.deductible_pct or 10,
            addons=state.addons or [],
            coverage_notes="Cobertura completa para daños materiales, RC, robo. Red amplia de talleres urbanos."
        )

    @staticmethod
    def carrier_pacifica(state: QuoteState) -> Offer:
        """Cotización de Pacífica Seguros"""
        premium = QuoteService.price_formula(state, carrier_bias=1.02)
        return Offer(
            carrier="Pacífica Seguros",
            plan=QuoteService.plan_for_value(state.vehicle_value_usd or 0),
            annual_premium_usd=premium,
            deductible_pct=state.deductible_pct or 10,
            addons=state.addons or [],
            coverage_notes="Fuerte en lunas y asistencia 24/7. Mejores SLA en costa."
        )

    @staticmethod
    def carrier_equinoccial(state: QuoteState) -> Offer:
        """Cotización de Equinoccial"""
        premium = QuoteService.price_formula(state, carrier_bias=1.00)
        return Offer(
            carrier="Equinoccial",
            plan=QuoteService.plan_for_value(state.vehicle_value_usd or 0),
            annual_premium_usd=premium,
            deductible_pct=state.deductible_pct or 10,
            addons=state.addons or [],
            coverage_notes="Buen balance precio/beneficio. Talleres certificados y auto sustituto opcional."
        )

    @staticmethod
    def aggregate_offers(state: QuoteState) -> List[Offer]:
        """Agrega ofertas de todas las aseguradoras"""
        offers = [
            QuoteService.carrier_andes(state),
            QuoteService.carrier_pacifica(state),
            QuoteService.carrier_equinoccial(state)
        ]
        offers.sort(key=lambda o: o.annual_premium_usd)
        return offers

    @staticmethod
    def recommend_text(state: QuoteState, offers: List[Offer]) -> str:
        """Genera texto de recomendación"""
        best = offers[0]
        reasons = []
        reasons.append(f"mejor precio estimado (USD {best.annual_premium_usd})")
        if (state.addons or []) and "cobertura_lunas" in (state.addons or []):
            if best.carrier != "Pacífica Seguros":
                reasons.append("considera Pacífica si priorizas lunas y asistencia 24/7")
        msg = (
            f"Recomiendo **{best.carrier} - Plan {best.plan}** por {', '.join(reasons)}. "
            f"Alternativas: {offers[1].carrier} y {offers[2].carrier}. "
            "Podemos emitir en línea validando documentos y pago."
        )
        return msg

    @staticmethod
    def generate_quote(state: QuoteState) -> QuoteResult:
        """Genera cotización completa"""
        offers = QuoteService.aggregate_offers(state)
        recommendation = QuoteService.recommend_text(state, offers)
        return QuoteResult(
            offers=offers,
            recommendation=recommendation,
            disclaimer=(
                "Estimado NO vinculante. Precio final sujeto a inspección, verificación de datos "
                "y políticas de la aseguradora. Sin intermediarios: contratación directa con la aseguradora."
            ),
        )
