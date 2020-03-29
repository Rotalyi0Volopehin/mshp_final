from django import forms, template
from django.forms import ModelForm


from main.models import Message

register = template.Library()

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
