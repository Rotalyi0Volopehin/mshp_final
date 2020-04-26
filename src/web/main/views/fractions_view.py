from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View

from main.db_tools.user_tools import DBUserTools
from main.views.menu import get_menu_context, get_user_menu_context

from collections import OrderedDict


class FractionPages(View):
    def collect_default_context(self, request) -> dict:
        context = {
            'menu': get_menu_context(),
            'user_menu': get_user_menu_context(request.user),
        }
        return context

    def sort_members_by_reputation(self, team: int):
        members = {}
        for user in User.objects.all():
            if DBUserTools.try_get_user_data(user) != None:
                user_data, error = DBUserTools.try_get_user_data(user)
                if user_data.team == team:
                    members[user.username] = user_data.reputation
        members = OrderedDict(sorted(members.items(), reverse=True, key=lambda value: value[1]))
        return members

    def fraction1_page(self, request):
        context = self.collect_default_context(request)
        context['pagename'] = 'Фракция1',
        context['members'] = self.sort_members_by_reputation(0),
        return render(request, 'pages/fractions/fraction1.html', context)

    def fraction2_page(self, request):
        context = self.collect_default_context(request)
        context['pagename'] = 'Фракция2',
        context['members'] = self.sort_members_by_reputation(1),
        return render(request, 'pages/fractions/fraction2.html', context)

    def fraction3_page(self, request):
        context = self.collect_default_context(request)
        context['pagename'] = 'Фракция3',
        context['members'] = self.sort_members_by_reputation(2),
        return render(request, 'pages/fractions/fraction3.html', context)