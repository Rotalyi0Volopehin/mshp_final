from main.views.menu import get_menu_context, get_user_menu_context
from django.shortcuts import render
from django.views import View
from django.forms import Form


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
    """
    pagename = "NOPAGENAME"
    form_class = Form
    template_name = "pages/index.html"
    display_user_menu = True

    get_handler = None
    post_handler = None

    def get(self, request, **kwargs):
        """**Обработчик get-запросов**\n
        Вызывает дополнительный обработчик get-запросов со следующими аргументами:\n
        - context (*dict*) - контекст
        - request (*HttpRequest*) - запрос
        - kwargs (*\\*\\*kwargs*)

        :param request: request на страницу
        :type request: HttpRequest
        :return: http-респонс страницы с пустой формой
        """
        context = self.collect_default_context(request)
        context["form"] = self.form_class()
        if self.get_handler is not None:
            self.get_handler(context, request, **kwargs)
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
            context["error"] = "Неверный формат отосланных данных!"
        elif self.post_handler is not None:
            self.post_handler(context, request, form, **kwargs)
        return render(request, self.template_name, context)

    def collect_default_context(self, request) -> dict:
        """**Метод, собирающий контекст по умолчанию**

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
