""" Обработка страниц с формами """

from django.shortcuts import render, redirect
from django.views import View
from django.forms import Form
from django.http import HttpResponse, HttpRequest
from main.views.menu import get_menu_context, get_user_menu_context


class FormView(View):
    """**View-класс для страниц с post-формами**\n
    abstract class\n
    Статические поля:\n
    - pagename (str) - имя страницы
    - form_class (type) - тип формы
    - template_name (str) - имя шаблона
    - display_user_menu (bool) - отображать ли навигационную панель пользователя
    - get_handler - дополнительный обработчик get-запросов (перегрузка опциональна)
    - set_handler - дополнительный обработчик post-запросов (перегрузка опциональна)

    Доп. обработчики могут возвращать HttpResponse, который будет отправлен вместо стандартного.
    Исключения, выбрасываемые доп. обработчиками, записываются в контекст в поле error.
    """
    pagename = "NOPAGENAME"
    form_class = Form
    template_name = "pages/index.html"
    display_user_menu = True
    login_required = False
    invalid_form_error = True

    get_handler = None
    post_handler = None

    def get(self, request: HttpRequest, **kwargs):
        """**Обработчик get-запросов**\n
        Вызывает дополнительный обработчик get-запросов со следующими аргументами:\n
        - context (*dict*) - контекст
        - request (*HttpRequest*) - запрос
        - kwargs (*\\*\\*kwargs*)

        :param request: request на страницу
        :type request: HttpRequest
        :return: http-респонс страницы с пустой формой
        """
        if self.login_required and not request.user.is_authenticated:
            return redirect("login")
        context = self.collect_default_context(request)
        context["form"] = self.form_class()
        if self.get_handler is not None:
            def handler():
                return self.get_handler(context, request, **kwargs)
            response = FormView.__call_handler(handler, context)
            if response is not None:
                return response
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        """**Обработчик post-запросов**\n
        Проверяет валидность пришедшего post-запроса.\n
        Вызывает дополнительный обработчик post-запросов со следующими аргументами:\n
        - context (*dict*) - контекст
        - request (*HttpRequest*) - запрос
        - form (*Form*) - форма, содержащая post-данные
        - kwargs (*\\*\\*kwargs*)

        :param request: request на страницу
        :type request: HttpRequest
        :return: http-респонс страницы с наполненной формой
        """
        context = self.collect_default_context(request)
        context["form"] = form = self.form_class(request.POST)
        if not form.is_valid():
            context["ok"] = False
            if self.invalid_form_error:
                context["error"] = "Неверный формат отосланных данных!"
        elif self.post_handler is not None:
            def handler():
                return self.post_handler(context, request, form, **kwargs)
            response = FormView.__call_handler(handler, context)
            if response is not None:
                return response
        return render(request, self.template_name, context)

    def collect_default_context(self, request) -> dict:
        """**Метод, собирающий контекст по умолчанию**\n
        :return: контекст по умолчанию
        :rtype: dict
        """
        context = {
            "pagename": self.pagename,
            "menu": get_menu_context(),
            "ok": True,
            "success": False,
            "error": None,
        }
        if self.display_user_menu:
            context["user_menu"] = get_user_menu_context(request.user)
        return context

    @staticmethod
    def __call_handler(handler, context: dict):
        try:
            response = handler()
            if isinstance(response, HttpResponse):
                return response
        except Exception as exception:
            context["ok"] = context["success"] = False
            context["error"] = str(exception)
