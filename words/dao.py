from dao.base import BaseDAO
from words.models import Words, Difficulties, GameSessions
from sqlalchemy import select, func, update
from database import async_session_maker


class WordDao(BaseDAO):
    model = Words

    @classmethod
    async def get_random_by_difficulty(cls, difficulty):
        async with async_session_maker() as session:
            query = (select(Words)
                     .join(Difficulties, Words.difficulties_id == Difficulties.id)
                     .where(Difficulties.name == difficulty)
                     .order_by(func.random())
                     .limit(1))

            result = await session.execute(query)
            return result.scalar()


class GameSessionDao(BaseDAO):
    model = GameSessions

    @classmethod
    async def create_game(cls, **data):
        async with async_session_maker() as session:
            game = GameSessions(**data)
            session.add(game)
            await session.commit()
            return game

    @classmethod
    async def update_game(cls,session_id,  **data):
        async with async_session_maker() as session:
            query = update(GameSessions).where(GameSessions.id == session_id).values(**data)
            await session.execute(query)
            await session.commit()













