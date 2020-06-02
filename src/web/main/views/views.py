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
    #CAD.clear_all_data()
    from main.models import GameSession
    from main.db_tools.game_session_tools import DBGameSessionTools
    from main.db_tools.user_participation_tools import DBUserParticipationTools
    gs = GameSession(title="GS01")
    gs.save()
    DBUserParticipationTools.try_sign_user_up_for_session(request.user, gs)
    DBGameSessionTools.start_session_active_phase(gs)
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
