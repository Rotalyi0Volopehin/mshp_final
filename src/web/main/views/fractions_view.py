from collections import OrderedDict

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from main.db_tools.user_tools import DBUserTools
from main.models import UserData
from main.views.menu import get_menu_context, get_user_menu_context


class FractionPages(View):
    @staticmethod
    def sort_members_by_reputation(team: int):
        members = {}
        for user in User.objects.all():
            if DBUserTools.try_get_user_data(user) != None and not user.is_superuser:
                user_data, error = DBUserTools.try_get_user_data(user)
                if user_data.team == team:
                    members[user.username] = user_data.reputation
        members = OrderedDict(sorted(members.items(), reverse=True, key=lambda value: value[1])[:10])
        return members

    @staticmethod
    def collect_default_context(request) -> dict:
        context = {
            'menu': get_menu_context(),
            'user_menu': get_user_menu_context(request.user),
        }
        return context

    @staticmethod
    def fraction0_page(request):
        context = FractionPages.collect_default_context(request)
        context['pagename'] = 'Cyber Corp'
        context['members'] = FractionPages.sort_members_by_reputation(0)
        return render(request, 'pages/fractions/fraction0.html', context)

    @staticmethod
    def fraction1_page(request):
        context = FractionPages.collect_default_context(request)
        context['pagename'] = 'Добрая воля'
        if request.user.is_authenticated:
            user_data, error = DBUserTools.try_get_user_data(request.user)
            context['team'] = user_data.team
            if user_data.team == 1:
                context['pagename'] = 'encrypted'
        context['members'] = FractionPages.sort_members_by_reputation(1)

        return render(request, 'pages/fractions/fraction1.html', context)

    @staticmethod
    def fraction2_page(request):
        context = FractionPages.collect_default_context(request)
        context['pagename'] = 'Зов Свободы'
        context['members'] = FractionPages.sort_members_by_reputation(2)
        return render(request, 'pages/fractions/fraction2.html', context)
