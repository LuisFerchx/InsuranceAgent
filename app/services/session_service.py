import time
import uuid
from typing import Dict, Any


class SessionService:
    _instance = None
    _sessions: Dict[str, Dict[str, Any]] = {}
    _ttl_seconds: int = 60 * 60

    def __new__(cls, ttl_seconds: int = 60 * 60):
        if cls._instance is None:
            cls._instance = super(SessionService, cls).__new__(cls)
            cls._ttl_seconds = ttl_seconds
        return cls._instance

    def __init__(self, ttl_seconds: int = 60 * 60):
        # No hacer nada en __init__ para mantener el singleton
        pass

    @property
    def sessions(self) -> Dict[str, Dict[str, Any]]:
        return self._sessions

    @property
    def ttl_seconds(self) -> int:
        return self._ttl_seconds

    def _now(self) -> float:
        return time.time()

    def new_session_id(self) -> str:
        return str(uuid.uuid4())

    def prune_sessions(self):
        """Elimina sesiones expiradas"""
        now = self._now()
        for sid in list(self._sessions.keys()):
            if now - self._sessions[sid].get("updated_at", now) > self._ttl_seconds:
                self._sessions.pop(sid, None)

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Obtiene una sesión por ID"""
        return self._sessions.get(session_id)

    def create_session(self, session_id: str, state: Any) -> None:
        """Crea una nueva sesión"""
        self._sessions[session_id] = {
            "state": state,
            "updated_at": self._now()
        }
        print(f"Session created: {self._sessions}")

    def update_session(self, session_id: str, state: Any) -> None:
        """Actualiza una sesión existente"""
        if session_id in self._sessions:
            self._sessions[session_id]["state"] = state
            self._sessions[session_id]["updated_at"] = self._now()

    def session_exists(self, session_id: str) -> bool:
        """Verifica si una sesión existe"""
        return session_id in self._sessions
