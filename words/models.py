from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, UUID
import uuid


class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, nullable=False)
    word = Column(String, nullable=False)
    difficulties_id = Column(ForeignKey("difficulties.id"), nullable=False)


class Difficulties(Base):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)


class GameSessions(Base):
    __tablename__ = "game_sessions"

    id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    word_id = Column(ForeignKey("words.id"), nullable=False)
    word_mask = Column(String, nullable=False)
    errors_left = Column(Integer, nullable=False, default=3)
    guessed_letters = Column(ARRAY(String))
    wrong_letters = Column(ARRAY(String))
    status = Column(String, nullable=False, default="active")
