from pydantic import BaseModel
from enum import StrEnum
from uuid import UUID


class Difficulty(StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Status(StrEnum):
    active = "active"
    won = "won"
    lost = "lost"


class StartRequest(BaseModel):
    difficulty: Difficulty


class StartResponse(BaseModel):
    session_id: UUID
    word_mask: str
    errors_left: int
    guessed_letters: list
    wrong_letters: list
    status: Status


class GuessRequest(BaseModel):
    session_id: UUID
    letter: str


class GuessResponse(StartResponse):
    message: str
    all_word: None | str = None


class StatsResponse(BaseModel):
    total_games: int
    wins: int
    losses: int
