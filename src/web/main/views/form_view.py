from main.views.menu import get_menu_context
from django.shortcuts import render
from django.views import View
from django.forms import Form


class FormView(View):
    pagename = "NOPAGENAME"
    form_class = Form
    template_name = "pages/index.html"

    get_handler = None
    post_handler = None

    def get(self, request):
        context = self.collect_default_context()
        context["form"] = self.form_class()
        if self.get_handler is not None:
            self.get_handler(context, request)
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.collect_default_context()
        context["form"] = form = self.form_class(request.POST)
        if not form.is_valid():
            context["ok"] = False
            context["error"] = "Неверный формат отосланных данных!"
        elif self.post_handler is not None:
            self.post_handler(context, request, form)
        return render(request, self.template_name, context)

    def collect_default_context(self) -> dict:
        return {
            "pagename": self.pagename,
            "menu": get_menu_context(),
            "ok": True,
            "success": False,
            "error": None,
        }
