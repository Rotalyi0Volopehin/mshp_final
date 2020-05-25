"""
import pygame


class Button:
    def __init__(self, game, x, y, text, image_press, image_unpress):
        super().__init__(game)
        self.size = [190, 45]  # Размер кнопки
        self.image_button = image_press # Загружаем изображение исходной кнопки
        self.text = text  # Текст кнопки
        self.x = x  # Позиция х кнопки
        self.y = y  # Позиция у кнопки
        self.clicked = False
        self.rect_button = pygame.Rect(self.x, self.y, self.size[0],
                                       self.size[1])  # Прямоугольник для создания коллизии с курсором
        self.rect_image_button = self.image_button.get_rect()
        #Создание кнопки при нажатии на нее
        self.image_click = image_press
        self.image_put_on_button = image_unpress

    def create_button(self):
       # Создает кнопку на экране
        font = pygame.font.Font(None, 36)
        text_button = font.render(self.text, True, (240, 240, 240))  # Создаем изображение с текстом
        text_rect = text_button.get_rect()  # Возвращаем прямоугольник который занимает текст
        text_rect.center = self.rect_image_button.center  # Делаем текст посередине кнопки
        self.image_button.blit(text_button, text_rect)
        self.image_click.blit(text_button, text_rect)
        self.image_put_on_button.blit(text_button, text_rect)

    def process_draw(self):
        if not (self.clicked):
            self.game.screen.blit(self.image_click, (self.x, self.y))
        else:
            self.game.screen.blit(self.image_put_on_button, (self.x, self.y))

    def process_logic(self):
        pass
"""

import pygame

from objects.button import Btn


class ImageButton(Btn):
    def __init__(self, game, image, geometry=(10, 10, 100, 100), text=None, function=None):
        super(ImageButton, self).__init__(game,geometry)
        self.image = image
        self.internal_button.function = function
        self.internal_button.text = text
        print(function)
        self.internal_button.render_text()

    def process_draw(self):
        self.internal_button.update(self.game.screen)
        self.game.screen.blit(self.image, (self.geometry[0], self.geometry[1]))
