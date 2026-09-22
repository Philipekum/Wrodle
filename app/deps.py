from app.services.game_logic import Game


GAME = {}


def get_db() -> dict[Game]:
    return GAME
