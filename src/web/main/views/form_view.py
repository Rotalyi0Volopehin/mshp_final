from main.views.menu import get_menu_context
from django.shortcuts import render
from django.views import View
from django.forms import Form


class FormView(View):
    """View-класс для страниц с post-формами
    abstract static class

    Static fields:\n
    - pagename (str) - имя страницы\n
    - form_class (type) - тип формы\n
    - template_name (str) - имя шаблона\n
    - get_handler - обработчик get-запросов (перегрузка опциональна)\n
    - set_handler - обработчик post-запросов (перегрузка опциональна)
    """
    pagename = "NOPAGENAME"
    form_class = Form
    template_name = "pages/index.html"

    get_handler = None
    post_handler = None

    def get(self, request):
        """Метод, принимающий get-request

        :param request: request на страницу '/time/'
        :type request: HttpRequest
        :return:
        """
        context = self.collect_default_context()
        context["form"] = self.form_class()
        if self.get_handler is not None:
            self.get_handler(context, request)
        return render(request, self.template_name, context)

    def post(self, request):
        """Метод, принимающий post-request

        :param request: request на страницу '/time/'
        :type request: HttpRequest
        :return:
        """
        context = self.collect_default_context()
        context["form"] = form = self.form_class(request.POST)
        if not form.is_valid():
            context["ok"] = False
            context["error"] = "Неверный формат отосланных данных!"
        elif self.post_handler is not None:
            self.post_handler(context, request, form)
        return render(request, self.template_name, context)

    def collect_default_context(self) -> dict:
        """Метод, собирающий контекст по умолчанию

        :return: контекст по умолчанию
        :rtype: dict
        """
        return {
            "pagename": self.pagename,
            "menu": get_menu_context(),
            "ok": True,
            "success": False,
            "error": None,
        }
