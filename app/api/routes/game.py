import hashlib
from fastapi import APIRouter, Request, Response, Depends
from app.config import MIN_WORD, MAX_WORD, MAX_ATTEMPTS
from app.deps import get_db
from app.services.game_logic import (
    process_attempt, 
    parse_word, 
    preprocess_word,
    Game,
    Attempt
)

router = APIRouter(tags=["game"])


@router.get("/init_game")
def init_game(request: Request, db: dict[Game] = Depends(get_db)) -> str:
    game = Game(
        user_ip=request.client.host,
        language="english",
        min_letters=MIN_WORD,
        max_letters=MAX_WORD,
        max_attempts=MAX_ATTEMPTS,
    )
    game_id = hashlib.sha256(f'{game.user_ip}:{game.min_letters}:{game.max_letters}:{game.language}'.encode()).hexdigest()
    db[game_id] = game
    return game_id


@router.post("/guess_word")
def guess_word(word: str, game_id: str, db: dict[Game] = Depends(get_db)) -> Game:
    game = db.get(game_id)

    if game is None:
        return "Game is not init"

    if game.is_finished:
        return "Game finished!"
    
    word = preprocess_word(word)
    attempt = Attempt(word=parse_word(word))
    
    if len(game.attempts) == game.max_attempts:
        return f"Game over: {len(game.attempts)}/{game.max_attempts} attempts"
    
    attempt = process_attempt(attempt)
    game.attempts.append(attempt)

    if attempt.word_is_guessed:
        return "You win!"

    return game
