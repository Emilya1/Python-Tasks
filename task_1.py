import random
import json

class Game:
    max_mistakes = 3
    def __init__(self,word_level):
        self.__word_level = word_level
        self.__word = ""
        self.__mask = []
        self.__guessed = set()
        self.__mistakes = 3
    def start_game(self, level):
        self.__word = random.choice(self.__word_level[level])
        self.__mask = ["_"] * len(self.__word)
        self.__guessed = set()
        self.__mistakes = 0
    def guess(self, letter):
        letter = letter.lower()
        if len(letter) != 1 or not letter.isalpha():
            return  "error"
        if letter in self.__guessed:
            return "буква уже была"
        self.__guessed.add(letter)
        if letter in self.__word:
            for i, y in enumerate(self.__word):
                if y == letter:
                    self.__mask[i] = letter
            return "угадано"
        self.__mistakes += 1
        return "буквы нет в слове"
    @property
    def mask(self):
        return "".join(self.__mask)
    @property
    def mistakes_left(self):
        return self.max_mistakes - self.__mistakes
    @property
    def guessed_letter(self):
        return sorted(self.__guessed)
    @property
    def is_won(self):
        return "".join(self.__mask) == self.__word

    @property
    def is_lost(self):
        return self.__mistakes >= self.max_mistakes

    @property
    def is_over(self):
        return self.is_won or self.is_lost

    @property
    def word(self):
        return self.__word

def load_words(path):
    try:
        with open(path, encoding= "utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {path} не найден")
        return None
    except json.JSONDecodeError:
        print(f"Файл {path} некорректный JSON")
        return None

word_level = load_words("word.json")
if word_level is None:
    exit()

level = input("Выберите сложность 1) easy 2)medium 3)hard): ").lower()
if level not in word_level:
    print("Такого уровня нет")
    exit()


game = Game(word_level)
game.start_game(level)

while not game.is_over:
    print(game.mask)
    letter = input("Введите букву: ")
    result = game.guess(letter)
    if result == "error":
        print("Введите только одну букву!")
    elif result == "буква уже была":
        print("Буква уже была")
    elif result == "буквы нет в слове":
        print(f"Буквы нет в слове, у вас осталось {game.mistakes_left} попыток")

if game.is_won:
    print(f"Вы выиграли! Слово - {game.word}")
else:
    print("Вы проиграли(")


