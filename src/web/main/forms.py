from django.core.exceptions import ValidationError
from attr import validators
from django import forms


class CommonFields:
    @staticmethod
    def get_description_field(required, label="Описание", attrs=None):
        return forms.CharField(widget=forms.Textarea(attrs=attrs), label=label, min_length=1,
                               max_length=4096, required=required)

    @staticmethod
    def get_login_field(required, label="Логин", attrs=None):
        return forms.CharField(label=label, min_length=1, max_length=64,
                               required=required, widget=forms.TextInput(attrs=attrs))

    @staticmethod
    def get_name_field(required, label="Псевдоним", attrs=None):
        return forms.CharField(label=label, min_length=1, max_length=64,
                               required=required, widget=forms.TextInput(attrs=attrs))

    @staticmethod
    def get_password_field(required, label="Пароль", attrs=None):
        return forms.CharField(widget=forms.PasswordInput(attrs=attrs), label=label,
                               min_length=1, max_length=64, required=required)

    @staticmethod
    def get_invisible_field(type_, id_, value=''):
        return type_(label="", widget=forms.HiddenInput(attrs={"id": id_, "value": value}))


class RegistrationForm(forms.Form):
    """**Форма для страницы '/registration/'**\n
    Поля формы:\n
    - login (*CharField TextInput*) - логин пользователя
    - password1 (*CharField PasswordInput*) - пароль пользователя
    - password2 (*CharField PasswordInput*) - костыль
    - name (*CharField TextInput*) - ник пользователя
    - email (*EmailField EmailInput*) - E-mail пользователя
    - team (*ChoiceField Select*) - фракция пользователя
    """
    login = CommonFields.get_login_field(True, attrs={"class": "form-control"})
    password1 = CommonFields.get_password_field(True, attrs={"class": "form-control"})
    password2 = CommonFields.get_password_field(True, "Повторите пароль", attrs={"class": "form-control"})
    name = CommonFields.get_name_field(True, attrs={"class": "form-control"})
    email = forms.EmailField(label="E-mail", min_length=1, max_length=64,
                             required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    team = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), label="Фракция",
                             required=True, choices=[(0, "Cyber Corp"), (1, "Добрая воля"), (2, "Зов Свободы")])


class CreateSessionForm(forms.Form):
    session_name = forms.CharField(label='Название сессии', min_length=1, max_length=64,
                               required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    user_per_team = forms.IntegerField(label='Игроков от фракции', min_value=1, max_value=8,
                                       required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    turn_period = forms.IntegerField(label='Время хода (секунды)', min_value=1, required=True,
                                     widget=forms.NumberInput(attrs={"class": "form-control"}))
    user_min_level = forms.IntegerField(label='Минимальный уровень участников', min_value=0,
                                           required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    user_max_level = forms.IntegerField(label='Максимальный уровень участников',min_value=0,
                                            required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    money_limit = forms.IntegerField(label='Лимит бюджета',min_value=-1, max_value=-1,
                                            required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))

    def check_highest_lower_level(self):
        max_lvl = self.cleaned_data["user_max_level"]
        min_lvl = self.cleaned_data["user_min_level"]
        if not ((max_lvl and min_lvl) or (min_lvl <= max_lvl)):
            raise forms.ValidationError("Выберите другой минимальный или максимальный уровень игроков!")


class ProfileForm(forms.Form):
    """**Форма для страницы '/profile/<int:uid>/'**\n
    Поля формы:\n
    - name (*CharField TextInput*) - ник пользователя
    - about (*CharField Textarea*) - дополнительная информация о пользователе
    - password (*CharField PasswordInput*) - текущий пароль пользователя
    - new_password (*CharField PasswordInput*) - новый пароль пользователя
    - action (*CharField HiddenInput*) - тип запроса ("save-chan", "save-pass", "del")
    """
    name = CommonFields.get_name_field(False)
    about = CommonFields.get_description_field(False, label="О себе")
    password = CommonFields.get_password_field(False)
    new_password = CommonFields.get_password_field(False)
    action = CommonFields.get_invisible_field(forms.CharField, "action_tag", '')


class LoginForm(forms.Form):
    login = CommonFields.get_login_field(True, attrs={"class": "form-control"})
    password = CommonFields.get_password_field(True, attrs={"class": "form-control"})
