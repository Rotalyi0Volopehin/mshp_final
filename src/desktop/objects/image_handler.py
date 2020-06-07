"""
Класс, ищущий упоминания персонажей в тексте
"""
import os
from objects.image import Image

CHARACTERS = {
    "Крейн:",
    "Секретарша:",
    "Китти Прайд:",
    "Курт:",
    "Картер:",
    "Никки:",
    "Симмонс:",
    "Лилия Свон:",
    "Рон Даггет:",
    "Джим Колан:"
}

CHARACTERS_TO_NAMES = {
    "Крейн:": "crayn.png",
    "Секретарша:": "secretary.png",
    "Китти Прайд:": "kitty.png",
    "Курт:": "kurt.png",
    "Картер:": "karter.png",
    "Никки:": "nikki.png",
    "Симмонс:": "simmons.png",
    "Лилия Свон:": "swa.png",
    "Рон Даггет:": "karter.png",
    "Джим Колан:": "jim.png"
}


class ImageHandler:
    """
    Класс поиска персонажей в тексте
    """
    def __init__(self, game):
        self.found_characters = []
        self.response = []
        self.game = game

    def find_characters(self, data):
        """
        Ищет имена и записывает их в массив
        :param data:
        :return:
        """
        self.found_characters = []
        for word in CHARACTERS:
            if data.find(word) != -1:
                self.found_characters.append(word)
        return self.handle_characters()

    def handle_characters(self):
        """
        Берет имена из массива и возвращает объекты картинок
        :return:
        """
        self.response = []
        iterator = 0
        if len(self.found_characters) == 1:
            char = self.found_characters[0]
            self.response.append(Image(self.game, os.path.join("images", CHARACTERS_TO_NAMES[char]),
                                       400, 250))
        else:
            for char in self.found_characters:
                self.response.append(Image(self.game, os.path.join("images", CHARACTERS_TO_NAMES[char]),
                                           100 + (400*iterator), 250))
                iterator += 1
        return self.response
