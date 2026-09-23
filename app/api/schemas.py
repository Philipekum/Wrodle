from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.config import PRESETS, GameDifficulty, GameRule, settings
from app.services.types import ValidatedWord


class Language(StrEnum):
    EN = "english"
    RU = "russian"


class LetterStatus(StrEnum):
    PENDING = "pending"
    GUESSED = "guessed"
    WRONG_PLACE = "wrong_place"
    WRONG = "wrong"


class Letter(BaseModel):
    letter: str = Field(min_length=1, max_length=1)
    status: LetterStatus = LetterStatus.PENDING


class Attempt(BaseModel):
    model_config = ConfigDict(frozen=True)

    word: ValidatedWord
    letters: list[Letter]

    @property
    @computed_field
    def word_is_guessed(self) -> bool:
        return bool(self.letters) and all(
            letter.status == LetterStatus.GUESSED for letter in self.letters
        )


class GameInitRequest(BaseModel):
    language: Language
    difficulty: GameDifficulty = settings.DEFAULT_DIFFICULTY


class AttemptRequest(BaseModel):
    word: ValidatedWord


class GameBase(BaseModel):
    game_id: str = Field(
        min_length=settings.GAME_ID_LEN, max_length=settings.GAME_ID_LEN
    )
    language: Language
    rules: GameRule = PRESETS[settings.DEFAULT_DIFFICULTY]
    attempts: list[Attempt] = Field(default_factory=list[Attempt])
    is_finished: bool = False


class GameResponse(GameBase):
    pass


class GameState(GameBase):
    target_word: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_attempt(self, attempt: Attempt) -> None:
        if self.is_finished:
            raise ValueError("Game is already finished")
        if len(self.attempts) >= self.rules.max_attempts:
            self.is_finished = True
            raise ValueError("No attempts left")

        self.attempts.append(attempt)

        if attempt.word_is_guessed:
            self.is_finished = True
