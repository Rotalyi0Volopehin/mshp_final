from django import forms

class CommonFields:
    @staticmethod
    def get_description_field(required, label="Описание", attrs=None):
        if attrs is None:
            return forms.CharField(widget=forms.Textarea, label=label, min_length=1, max_length=4096, required=required)
        return forms.CharField(widget=forms.Textarea(attrs=attrs), label=label, min_length=1, max_length=4096, required=required)

    @staticmethod
    def get_login_field(required, label="Логин", attrs={}):
        return forms.CharField(label=label, min_length=1, max_length=64, required=required, widget=forms.TextInput(attrs=attrs))

    @staticmethod
    def get_name_field(required, label="Имя", attrs={}):
        return forms.CharField(label=label, min_length=1, max_length=64, required=required, widget=forms.TextInput(attrs=attrs))

    @staticmethod
    def get_password_field(required, label="Пароль", attrs={}):
        return forms.CharField(widget=forms.PasswordInput(attrs=attrs), label=label, min_length=1, max_length=64, required=required)

    @staticmethod
    def get_filter_option_field(label, attrs=None):
        if attrs is None:
            return forms.ChoiceField(widget=forms.Select, label=label, required=False,
                    choices=[(0, "--- (0)"), (1, "исключение (1)"), (-1, "исключение иных (-1)")])
        return forms.ChoiceField(widget=forms.Select(attrs=attrs), label=label, required=False,
                                 choices=[(0, "--- (0)"), (1, "исключение (1)"), (-1, "исключение иных (-1)")])


    @staticmethod
    def get_invisible_field(type_, id, value=''):
        return type_(label="", widget=forms.HiddenInput(attrs={ "id": id, "value": value }))

class RegistrationForm(forms.Form):
    login = CommonFields.get_login_field(True, attrs={"class": "form-control"})
    password1 = CommonFields.get_password_field(True, attrs={"class": "form-control"})
    password2 = CommonFields.get_password_field(True, "Повторите пароль", attrs={"class": "form-control"})
    name = CommonFields.get_name_field(True, attrs={"class": "form-control"})
    email = forms.CharField(label="E-mail", min_length=1, max_length=64, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    team = forms.IntegerField(max_value=2, min_value=0)


class ProfileForm(forms.Form):
    name = CommonFields.get_name_field(False)
    about = CommonFields.get_description_field(False, label="О себе")
    password = CommonFields.get_password_field(False)
    new_password = CommonFields.get_password_field(False)
    action = CommonFields.get_invisible_field(forms.CharField, "action_tag", '')
