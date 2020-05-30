import pygame


# TODO: удалить по причине ущербности


class Button:
    def __init__(self, x, y, text, image_press, image_unpress):
        self.size = [190, 45]  # Размер кнопки
        self.image_button = pygame.image.load(image_press)  # Загружаем изображение исходной кнопки
        self.text = text  # Текст кнопки
        self.x = x  # Позиция х кнопки
        self.y = y  # Позиция у кнопки
        self.clicked = False
        self.rect_button = pygame.Rect(self.x, self.y, self.size[0],
                                       self.size[1])  # Прямоугольник для создания коллизии с курсором
        self.rect_image_button = self.image_button.get_rect()
        """Создание кнопки при нажатии на нее"""
        self.image_click = pygame.image.load(image_press)
        self.image_put_on_button = pygame.image.load(image_unpress)

    def create_button(self):
        """Создает кнопку на экране"""
        font = pygame.font.Font(None, 36)
        text_button = font.render(self.text, True, (240, 240, 240))  # Создаем изображение с текстом
        text_rect = text_button.get_rect()  # Возвращаем прямоугольник который занимает текст
        text_rect.center = self.rect_image_button.center  # Делаем текст посередине кнопки
        self.image_button.blit(text_button, text_rect)
        self.image_click.blit(text_button, text_rect)
        self.image_put_on_button.blit(text_button, text_rect)

    def drawbutton(self, screen):
        img = self.image_put_on_button if self.clicked else self.image_click
        screen.blit(self.image_click, (self.x, self.y))
