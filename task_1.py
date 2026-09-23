import json
import sys

from game import *


def load_words(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return None
    except json.JSONDecodeError:
        print(f"Файл {path} некорректный JSON")
        return None


word_level = load_words("word.json")

if word_level is None:
    sys.exit()

level = input("Выберите сложность 1) easy 2)medium 3)hard): ").lower()

if level not in word_level:
    print("Такого уровня нет")
    sys.exit()

if __name__ == "__main__":
    game = Game(word_level)
    game.start_game(level)

    while not game.is_over:
        print(game.mask)
        letter = input("Введите букву: ")
        result = game.guess(letter)

        if result == TechnicalReturns.error:
            print("Введите только одну букву!")
        elif result == TechnicalReturns.repeat:
            print("Буква уже была")
        elif result == TechnicalReturns.notInWord:
            print(f"Буквы нет в слове, у вас осталось {game.mistakes_left} попыток")

    if game.is_won:
        print(f"Вы выиграли! Слово - {game.word}")
    else:
        print("Вы проиграли(")
