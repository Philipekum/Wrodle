from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import AttemptRequest, GameInitRequest, GameResponse, GameState
from app.config import PRESETS
from app.deps import get_db
from app.services.game_logic import (
    generate_game_id,
    get_target_word,
    resolve_attempt,
)

router = APIRouter(tags=["game"])


@router.post("/games/init", response_model=GameResponse)
def init_game(
    game_settings: GameInitRequest,
    db: dict[str, GameState] = Depends(get_db),
) -> GameResponse:
    
    game_id = generate_game_id()

    while game_id in db:
        game_id = generate_game_id()

    state = GameState(
        game_id=game_id,
        language=game_settings.language,
        rules=PRESETS[game_settings.difficulty],
        target_word=get_target_word(),
    )

    db[game_id] = state

    return GameResponse.model_validate(state, from_attributes=True)


@router.post("/games/{game_id}/attempts", response_model=GameResponse)
def make_attempt(
    game_id: str, request: AttemptRequest, db: dict[str, GameState] = Depends(get_db)
) -> GameResponse:

    state = db.get(game_id)

    if state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    if len(state.attempts) >= state.rules.max_attempts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No attempts left",
        )

    if state.is_finished:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Game is already finished",
        )

    attempt = resolve_attempt(request.word, state.target_word)
    state.attempts.append(attempt)

    if attempt.word_is_guessed:
        state.is_finished = True

    return GameResponse.model_validate(state, from_attributes=True)
