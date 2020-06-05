from main.db_tools.cad import CAD
from django.http import HttpResponse

from main.views.menu import get_menu_context, get_user_menu_context
from django.shortcuts import render


def index_page(request):
    """**View-функция страницы '/'**

    :param request: request на страницу '/'
    :type request: HttpRequest
    :return: response
    :rtype: HttpResponse
    """
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/index.html', context)


def cad_page(request):
    CAD.clear_all_data()
    """
    from django.contrib.auth.models import User
    from main.db_tools.user_participation_tools import DBUserParticipationTools
    from main.models import GameSession
    users = User.objects.all()[:3]
    gs = GameSession.objects.get(title="GS01")
    for user in users:
        DBUserParticipationTools.try_sign_user_up_for_session(user, gs)
    """
    """
    from main.db_tools.game_session_tools import DBGameSessionTools
    from main.models import GameSession
    gs = GameSession.objects.get(title="GS01")
    DBGameSessionTools.start_session_active_phase(gs)
    """
    return HttpResponse("SUCCESS! All data is cleared")


def forum_page(request):
    context = {
        'pagename': 'Форум',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/forum.html', context)


def chat_page(request):
    context = {
        'pagename': 'Закрытые каналы',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/chat.html', context)
