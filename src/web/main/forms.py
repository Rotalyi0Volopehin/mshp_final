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
    login = CommonFields.get_login_field(True, attrs={"class": "form-control"})
    password1 = CommonFields.get_password_field(True, attrs={"class": "form-control"})
    password2 = CommonFields.get_password_field(True, "Повторите пароль", attrs={"class": "form-control"})
    name = CommonFields.get_name_field(True, attrs={"class": "form-control"})
    email = forms.CharField(label="E-mail", min_length=1, max_length=64,
                            required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    team = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), label="Фракция",
                             required=True, choices=[(0, "0"), (1, "1"), (2, "2")])

