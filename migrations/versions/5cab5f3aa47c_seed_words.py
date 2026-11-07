"""seed words

Revision ID: 5cab5f3aa47c
Revises: 4717043d84a8
Create Date: 2026-11-07 12:51:02.985980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5cab5f3aa47c'
down_revision: Union[str, Sequence[str], None] = '4717043d84a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    difficulties = sa.table("difficulties", sa.column("id", sa.Integer),
                            sa.column("name", sa.String), )
    words = sa.table("words", sa.column("word", sa.String),
                     sa.column("difficulties_id", sa.Integer), )
    op.bulk_insert(difficulties, [
        {"id": 1, "name": "easy"},
        {"id": 2, "name": "medium"},
        {"id": 3, "name": "hard"}
    ])

    WORDS = {
        1: ["дом", "жук", "лето", "рука", "река", "небо", "клей", "слон", "кит", "кот"],
        2: ["семья", "фильм", "город", "книга", "сумка", "лампа", "песня", "вилка", "ложка"],
        3: ["квартира", "телевизор", "брелок", "машина", "ножницы", "телефон", "атрибут"],
    }
    rows = []
    for difficulty_id, word_list in WORDS.items():
        for word in word_list:
            rows.append({"word": word, "difficulties_id": difficulty_id})

    op.bulk_insert(words, rows)



def downgrade() -> None:
    op.execute("DELETE FROM words")
    op.execute("DELETE FROM difficulties")
