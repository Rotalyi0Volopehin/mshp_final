import pygame
from pygame_textinput import TextInput as TInput
from constants import Color
from objects.base import DrawObject


class TextInput(DrawObject):
    """Класс строки ввода"""
    BUTTON_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.RED,
        "clicked_color": Color.GREEN,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE
    }

    def __init__(self, game, antialias, x, y):
        """Инициализация"""
        super().__init__(game)
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.internal_txtinput = TInput(self.game, antialias=antialias)
        self.internal_txtinput.keyrepeat_interval_ms = 500
        self.down_keys = dict()

    def set_antialias(self, antialias):
        """Установка активности поля ввода"""
        self.internal_txtinput.antialias = antialias

    def process_event(self, event):
        """Процесс событий"""
        if event.type == pygame.KEYDOWN:
            if self.internal_txtinput.antialias:
                self.handle_down_key(event)
        elif (event.type == pygame.KEYUP) and self.internal_txtinput.antialias and (event.key in self.down_keys):
            self.down_keys[event.key] = None
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            antialias = (self.x <= event.pos[0] <= self.x + self.internal_txtinput.font_size * 10) and\
                    (self.y <= event.pos[1] <= self.y + self.internal_txtinput.font_size)
            self.internal_txtinput.antialias = antialias
            del antialias
        else:
            self.internal_txtinput.update(event)

    def process_draw(self):
        """Процесс рислоавния"""
        self.game.screen.blit(self.internal_txtinput.get_surface(), self.pos)

    def update_internal_txtinput(self):
        """Обновление текста"""
        mock_event = pygame.event.Event(pygame.WINDOWEVENT, {})
        self.internal_txtinput.update(mock_event)

    def handle_down_key(self, event):
        """Обработка нажатия кнопки"""
        ucode = event.unicode
        text = self.internal_txtinput.input_string
        cur_pos = self.internal_txtinput.cursor_position
        not_cur_first = cur_pos > 0
        not_cur_last = cur_pos < len(text)
        if event.key == pygame.K_BACKSPACE:
            if not_cur_first:
                self.internal_txtinput.input_string = f"{text[:cur_pos - 1]}{text[cur_pos:]}"
                self.internal_txtinput.cursor_position -= 1
        elif event.key == pygame.K_DELETE:
            if not_cur_last:
                self.internal_txtinput.input_string = f"{text[:cur_pos]}{text[cur_pos + 1:]}"
        elif event.key == pygame.K_LEFT:
            if not_cur_first:
                self.internal_txtinput.cursor_position -= 1
        elif event.key == pygame.K_RIGHT:
            if not_cur_last:
                self.internal_txtinput.cursor_position += 1
        elif event.key == pygame.K_HOME:
            self.internal_txtinput.cursor_position = 0
        elif event.key == pygame.K_END:
            self.internal_txtinput.cursor_position = len(text)
        elif str.isprintable(ucode) and (ucode not in self.down_keys.values()):
            self.down_keys[event.key] = ucode
            self.internal_txtinput.input_string = f"{text[:cur_pos]}{ucode}{text[cur_pos:]}"
            self.internal_txtinput.cursor_position += 1
        self.update_internal_txtinput()
