from django.shortcuts import redirect, render

import main.forms as forms
from main.views.form_view import FormView

class CreateSessionFormPage(FormView):

    pagename = "Создание сессии"
    form_class = forms.CreateSessionForm
    template_name = "pages/create_session.html"










#sesssion_name = form.data["sesssion_name"]
#user_per_team = int(form.data["user_per_team"])
#turn_period = int(form.data["turn_period"])
#user_lowest_level = int(form.data["user_lowest_level"])
#user_highest_level = int(form.data["user_highest_level"])
#money_limit = int(form.data["money_limit"])