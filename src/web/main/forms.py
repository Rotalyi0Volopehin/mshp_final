from django import forms
from django.forms import ModelForm
from src.web.main.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}


    @register.simple_tag
    def get_companion(user, chat):
        for u in chat.members.all():
            if u != user:
                return u
        return None
