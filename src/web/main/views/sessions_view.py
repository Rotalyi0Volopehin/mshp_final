from django.contrib.auth import login as log_user_in
from django.contrib.auth.models import User

import main.forms as forms
from main.db_tools.user_tools import DBUserTools
from main.views.form_view import FormView
from main.views.menu import get_user_menu_context


class RegistrationFormPage(FormView):
    """**View-класс страницы '/registration/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """
    pagename = "Поиск сессии"
    form_class = forms.SessionsForm
    template_name = "pages/sessions.html"
    ROWS_PER_PAGE = 8

    @staticmethod
    def get_handler(context: dict, request):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.get`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/profile/<int:uid>/'
        :type request: HttpRequest
        """
        page_ind = int(request.GET.get("0"))
        context["table"] = table = RegistrationFormPage.ROWS_PER_PAGE * [None]
        for i in range(RegistrationFormPage.ROWS_PER_PAGE):
            pass
