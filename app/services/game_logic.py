from enum import Enum
from collections import Counter
from dataclasses import dataclass, field


class Language(Enum):
    EN = "english"
    RU = "russian"


@dataclass
class Attempt:
    word: list[Letter]
    word_is_guessed: bool = False


@dataclass
class Game:
    user_ip: str
    language: Language
    min_letters: int
    max_letters: int
    max_attempts: int
    attempts: list[Attempt] = field(default_factory=list)
    is_finished: bool = False


class LetterStatus(Enum):
    PENDING = "pending"
    GUESSED = "guessed"
    WRONG_PLACE = "wrong_place"
    WRONG = "wrong"


@dataclass
class Letter:
    letter: str
    status: LetterStatus = "pending"


def preprocess_word(word: str) -> str:
    return word.strip().casefold()


def get_word() -> str:
    return "bebra"


def parse_word(word: str) -> list[Letter]:
    return [Letter(letter) for letter in word]


def process_attempt(attempt: Attempt) -> Attempt:
    right_word = get_word()
    right_letters_count = Counter(right_word)

    for i, letter in enumerate(attempt.letters):
        if letter.letter == right_word[i]:
            letter.status = "guessed"
            right_letters_count[letter.letter] -= 1

    guessed = 0

    for letter in attempt.letters:
        if letter.status == "guessed":
            guessed += 1
            continue

        if letter.letter in right_word and right_letters_count[letter.letter] > 0:
            letter.status = "wrong_place"
            right_letters_count[letter.letter] -= 1

    attempt.word_is_guessed = guessed == len(attempt.word)
    return attempt
