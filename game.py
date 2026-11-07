import random
from enum import StrEnum


class TechnicalReturns(StrEnum):
    error = "error"
    repeat = "you're repeating"
    guessed = "you're guessed the word"
    notInWord = " letter not in the word"


class Game:
    def __init__(self, word_level: dict[str, list[str]], max_mistakes: int = 3):
        self.__game_level: dict[str, list[str]] = word_level
        self.__max_mistakes: int = max_mistakes
        self.__word: str = ""
        self.__mask: list[str] = []
        self.__guessed: set[str] = set()
        self.__mistakes: int = 3

    def start_game(self, level: str):
        self.__word = random.choice(self.__game_level[level])
        self.__mask = ["_"] * len(self.__word)
        self.__guessed = set()
        self.__mistakes = 0

    def guess(self, letter) -> str:
        letter = letter.lower()

        if len(letter) != 1 or not letter.isalpha():
            return TechnicalReturns.error

        if letter in self.__guessed:
            return TechnicalReturns.repeat

        self.__guessed.add(letter)

        if letter in self.__word:
            for i, word_letter in enumerate(self.__word):
                if word_letter == letter:
                    self.__mask[i] = letter
            return TechnicalReturns.guessed

        self.__mistakes += 1
        return TechnicalReturns.notInWord

    @property
    def mask(self) -> str:
        return "".join(self.__mask)

    @property
    def mistakes_left(self) -> int:
        return self.__max_mistakes - self.__mistakes

    @property
    def guessed_letter(self) -> list[str]:
        return sorted(self.__guessed)

    @property
    def is_won(self) -> bool:
        return "".join(self.__mask) == self.__word

    @property
    def is_lost(self) -> bool:
        return self.__mistakes >= self.__max_mistakes

    @property
    def is_over(self) -> bool:
        return self.is_won or self.is_lost

    @property
    def word(self) -> str:
        return self.__word
