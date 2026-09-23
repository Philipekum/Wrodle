from enum import StrEnum

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GameDifficulty(StrEnum):
    QUICK = "quick"
    CLASSIC = "classic"
    HARDCORE = "hardcore"


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "Wrodle"

    DEFAULT_DIFFICULTY: GameDifficulty = GameDifficulty.CLASSIC
    MIN_WORD = 3
    MAX_WORD = 10
    MIN_ATTEMPTS = 1
    MAX_ATTEMPTS = 12
    GAME_ID_LEN = 5

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = AppSettings()


class GameRule(BaseModel):
    min_word: int = Field(ge=settings.MIN_WORD, le=settings.MAX_WORD)
    max_word: int = Field(ge=settings.MIN_WORD, le=settings.MAX_WORD)
    max_attempts: int = Field(ge=settings.MIN_ATTEMPTS, le=settings.MAX_ATTEMPTS)

    @model_validator(mode="after")
    def validate_word_lengths(self) -> GameRule:
        if self.min_word > self.max_word:
            raise ValueError("min_word can't be more than max_word")
        return self


PRESETS: dict[GameDifficulty, GameRule] = {
    GameDifficulty.QUICK: GameRule(min_word=3, max_word=4, max_attempts=5),
    GameDifficulty.CLASSIC: GameRule(min_word=5, max_word=5, max_attempts=6),
    GameDifficulty.HARDCORE: GameRule(min_word=6, max_word=7, max_attempts=5),
}
