from fastapi import APIRouter, Response
from words.schemas import StartRequest, GuessRequest, StatsResponse, StartResponse, GuessResponse
from words.service import GameService


router = APIRouter(
    prefix="/api/game",
    tags=["Game & 'Висилица'"],

)
routerGet = APIRouter(
    prefix="/api",
    tags=["Статистика"],
)

@router.post("/start")
async def start_game(word_difficulty: StartRequest) -> StartResponse:
    return await GameService.start(word_difficulty.difficulty)

@router.post("/guess")
async def guess_word(guess_request: GuessRequest) -> GuessResponse:
    return await GameService.guess(guess_request.session_id, guess_request.letter )


@routerGet.get("/stats")
async def stats() -> StatsResponse:
    return await GameService.stats()