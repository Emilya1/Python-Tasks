from words.dao import WordDao
from fastapi import HTTPException, status
from words.dao import GameSessionDao
from words.schemas import StartResponse, StatsResponse,GuessResponse

class GameService:

    @classmethod
    async def start(cls, difficulty):
        word = await WordDao.get_random_by_difficulty(difficulty)
        if word is None:
            Incorrect_Exception = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ошибка",
            )
            raise Incorrect_Exception
        game = await GameSessionDao.create_game(
            word_id=word.id,
            word_mask=make_mask(word.word,[]),
            guessed_letters=[],
            wrong_letters=[],
        )
        return StartResponse(session_id=game.id,
                             word_mask=game.word_mask,
                             errors_left=game.errors_left,
                             guessed_letters=[],
                             wrong_letters=[],
                             status=game.status
                             )


    @classmethod
    async def stats(cls):
        wins = await GameSessionDao.find_all(status="won")
        losses = await GameSessionDao.find_all(status="lost")
        total_games = len(wins) + len(losses)
        return StatsResponse(total_games=total_games,
                             wins=len(wins),
                             losses=len(losses)
                             )

    @classmethod
    async def guess(cls, session_id, letter):
        letter = letter.lower()
        if not letter.isalpha() or len(letter) != 1:
            Incorrect_Exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="введите одну букву",
            )
            raise Incorrect_Exception
        game = await GameSessionDao.find_one_or_none(id=session_id)
        if game is None:
            Incorrect_Game = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="игра не найдена",)
            raise Incorrect_Game
        if game.status != "active":
            Incorrect_Game_Status = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="игра не найдена",)
            raise Incorrect_Game_Status
        word = await WordDao.find_one_or_none(id=game.word_id)
        guessed = list(game.guessed_letters)
        wrong = list(game.wrong_letters)
        errors_left = game.errors_left
        game_status = game.status


        if letter in guessed or letter in wrong:
            message = "Буква уже была"
        elif letter in word.word:
            guessed.append(letter)
            message = "Буква угадана"
            if "_" not in make_mask(word.word, guessed):
                game_status = "won"
                message = "Победа"
        else:
            wrong.append(letter)
            errors_left -= 1
            message = "Ошибка"
            if errors_left < 0:
                game_status = "lost"
                message = "Поражение"

        word_mask = make_mask(word.word, guessed)

        await GameSessionDao.update_game(
            session_id,
            word_mask=word_mask,
            guessed_letters=guessed,
            wrong_letters=wrong,
            errors_left=errors_left,
            status=game_status,
        )

        return GuessResponse(
            session_id=session_id,
            word_mask=word_mask,
            errors_left=max(errors_left, 0),
            guessed_letters=guessed,
            wrong_letters=wrong,
            status=game_status,
            message=message,
            all_word=word.word if game_status != "active" else None,)


def make_mask(word, guessed_letters):
    maska = []
    for i in word:
        if i in guessed_letters:
            maska.append(i)
        else:
            maska.append("_")
    return " ".join(maska)




