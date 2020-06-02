from objects.text_input import TextInput


class PasswordInput(TextInput):
    """Класс наследуемый от TextInput"""
    def __init__(self, *args, **kwargs):
        """Инициализация"""
        super().__init__(*args, **kwargs)
        self.__hidden_string = ""
        self.hide_input = True

    def process_draw(self):
        """Процесс отрисовки"""
        if self.hide_input:
            self.__update_hidden_string()
            text = self.internal_txtinput.input_string
            self.internal_txtinput.input_string = self.__hidden_string
            self.update_internal_txtinput()
            super().process_draw()
            self.internal_txtinput.input_string = text
            return
        super().process_draw()

    def __update_hidden_string(self):
        """Обновление скрытой строки"""
        new_len = len(self.internal_txtinput.input_string)
        if new_len != len(self.__hidden_string):
            self.__hidden_string = "*" * new_len
