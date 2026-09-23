from typing import Annotated

from pydantic import AfterValidator

from app.config import settings


def _validate_word(value: str) -> str:
    cleaned = value.strip().casefold()

    if not (settings.MIN_WORD <= len(cleaned) <= settings.MAX_WORD):
        raise ValueError(f"length must be {settings.MIN_WORD}...{settings.MAX_WORD}")

    if not cleaned.isalpha():
        raise ValueError("word must contain only letters")

    return cleaned


ValidatedWord = Annotated[str, AfterValidator(_validate_word)]
