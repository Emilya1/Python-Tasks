import random

array=["человек","дом","книга","собака","тарелка","тетрадь","лампа","лето","телефон","жук","ручка","зарядка"]
random_word = random.choice(array)
print(random_word)
count = 0
a = ["_"] * len(random_word)
guessed = set()
while count < 3:
    word = "".join(a)
    if word == random_word:
        print(a)
        print(f"Вы выиграли слово - {random_word}")
        break
    print(a)
    input_letter = input(f"Введите букву: ")
    if len(input_letter) == 1 and input_letter.isalpha():
        if input_letter in guessed:
            print("Буква уже была")
            continue
        guessed.add(input_letter)
        if input_letter in random_word:
            for i in range(len(random_word)):
                if input_letter == random_word[i]:
                    a[i] = input_letter
        else:
            count +=1
            print(f"у вас осталось {3 -count} попыток")
    else: print("Ведите только одну букву!")
else:
    print("Вы проиграли( ")

