import secrets
from collections import Counter

from app.api.schemas import Attempt, Letter, LetterStatus
from app.config import settings


def get_target_word() -> str:
    return "bebra"


def generate_game_id() -> str:
    return secrets.token_urlsafe(settings.GAME_ID_LEN)[: settings.GAME_ID_LEN].lower()


def resolve_attempt(guess: str, target: str) -> Attempt:
    target_counts = Counter(target)
    letters: list[Letter] = []

    for i, ch in enumerate(guess):
        if ch == target[i]:
            letters.append(Letter(letter=ch, status=LetterStatus.GUESSED))
            target_counts[ch] -= 1
        else:
            letters.append(Letter(letter=ch))

    for letter in letters:
        if letter.status == LetterStatus.GUESSED:
            continue

        if target_counts[letter.letter] > 0:
            letter.status = LetterStatus.WRONG_PLACE
            target_counts[letter.letter] -= 1

        else:
            letter.status = LetterStatus.WRONG

    return Attempt(word=guess, letters=letters)
