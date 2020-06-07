""" Страница фракций """

from collections import OrderedDict

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from main.db_tools.user_tools import DBUserTools
from main.views.menu import get_menu_context, get_user_menu_context


class FractionPages(View):
    """**View-класс страницы фракций**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """

    @staticmethod
    def sort_members_by_reputation(team: int, context):
        """**Сортировка участников фракции по репутации**

        :param team: номер фракции
        :type team: int
        :param context: контекст страницы
        :type context: dict
        :return: отсортированные по репутации участники фракции
        :rtype: OrderedDict
        """
        members = {}
        for user in User.objects.all():
            if DBUserTools.try_get_user_data(user) is not None and not user.is_superuser:
                user_data, context['error'] = DBUserTools.try_get_user_data(user)
                if user_data.team == team:
                    members[user.username] = user_data.victories_count
        members = OrderedDict(sorted(members.items(),
                                     reverse=True, key=lambda value: value[1])[:10])
        return members

    @staticmethod
    def collect_default_context(request) -> dict:
        """**Формирование стандартного контекста страницы**

        :param request: запрос на страницу
        :type request: HttpRequest
        :return: контекст страницы
        :rtype: dict
        """
        context = {
            'menu': get_menu_context(),
            'user_menu': get_user_menu_context(request.user),
        }
        return context

    @staticmethod
    def fraction0_page(request):
        """**View функция первой фракции**

        :param request: запрос на страницу
        :type request: HttpRequest
        :return: response
        :rtype: HttpResponse
        """
        context = FractionPages.collect_default_context(request)
        context['pagename'] = 'Cyber Corp'
        context['members'] = FractionPages.sort_members_by_reputation(0, context)
        return render(request, 'pages/fractions/fraction0.html', context)

    @staticmethod
    def fraction1_page(request):
        """**View функция второй фракции**

        :param request: запрос на страницу
        :type request: HttpRequest
        :return: response
        :rtype: HttpResponse
        """
        context = FractionPages.collect_default_context(request)
        context['pagename'] = 'Добрая воля'
        if request.user.is_authenticated:
            user_data, context['error'] = DBUserTools.try_get_user_data(request.user)
            context['team'] = user_data.team
            if user_data.team == 1:
                context['pagename'] = 'encrypted'
        context['members'] = FractionPages.sort_members_by_reputation(1, context)

        return render(request, 'pages/fractions/fraction1.html', context)

    @staticmethod
    def fraction2_page(request):
        """**View функция третьей фракции**

        :param request: запрос на страницу
        :type request: HttpRequest
        :return: response
        :rtype: HttpResponse
        """

        context = FractionPages.collect_default_context(request)
        context['pagename'] = 'Зов Свободы'
        context['members'] = FractionPages.sort_members_by_reputation(2, context)
        return render(request, 'pages/fractions/fraction2.html', context)
