from app.api.schemas import GameState

_GAME_STATES: dict[str, GameState] = {}


def get_db() -> dict[str, GameState]:
    return _GAME_STATES
