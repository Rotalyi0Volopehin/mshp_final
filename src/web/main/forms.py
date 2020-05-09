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
    - email (*CharField TextInput*) - E-mail пользователя
    - team (*ChoiceField Select*) - фракция пользователя
    """
    login = CommonFields.get_login_field(True, attrs={"class": "form-control"})
    password1 = CommonFields.get_password_field(True, attrs={"class": "form-control"})
    password2 = CommonFields.get_password_field(True, "Повторите пароль", attrs={"class": "form-control"})
    name = CommonFields.get_name_field(True, attrs={"class": "form-control"})
    email = forms.CharField(label="E-mail", min_length=1, max_length=64,
                            required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    team = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), label="Фракция",
                             required=True, choices=[(0, "0"), (1, "1"), (2, "2")])


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

