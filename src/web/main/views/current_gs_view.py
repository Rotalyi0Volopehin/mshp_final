""" Страница текущей сессии """

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.views.menu import get_menu_context, get_user_menu_context
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.user_tools import DBUserTools


@login_required
def current_gs_page(request):
    """**View-функция страницы текущей сессии**

    :param request: request на страницу сессии
    :type request: HttpRequest
    :return: response
    :rtype: HttpResponse
    """
    context = {
        'pagename': 'Текущая сессия',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
        'error': None,
        'ok': True,
        'state': -1,
    }
    user_data, error = DBUserTools.try_get_user_data(request.user)
    if user_data is None:
        context['ok'] = False
        context['error'] = error
    else:
        participation = DBUserParticipationTools.get_user_participation(request.user)
        if participation is None:
            context['state'] = 0
        elif participation.game_session.phase == 0:
            context['state'] = 1
            expectation_game_session_state(context, participation.game_session)
        else:
            context['state'] = 2
            playing_game_session_state(context, participation.game_session, user_data)
    return render(request, 'pages/current_session/game_session_body.html', context)


def expectation_game_session_state(context, game_session):
    """**Добавление данных о сессии в контекст страницы**

    :param context: контекст страницы
    :type context: dict
    :param game_session: игровая сессия
    :type game_session: GameSession
    """
    add_game_session_name_to_context(context, game_session)
    context['players_gathered'] = game_session.players_gathered


def playing_game_session_state(context, game_session, user_data):
    """**Формирование данных об игровой сессии**

    :param context: контекст страницы
    :type context: dict
    :param game_session: игровая сессия
    :type game_session: GameSession
    :param user_data: информация об игроке
    :type user_data: UserData
    """
    add_game_session_name_to_context(context, game_session)
    teams = (("Cyber Corp", []), ("Добрая Воля", []), ("Зов Свободы", []))
    participations = game_session.get_participants()
    for participation in participations:
        name = participation.user_data.user.username
        self = participation.user_data == user_data
        teams[participation.user_data.team][1].append((name, self))
    context['teams'] = teams


def add_game_session_name_to_context(context, game_session):
    """**Добавление названия игровой сессии в контекст страницы**

    :param context: контекст страницы
    :type context: dict
    :param game_session: игровая сессия
    :type game_session: GameSession
    """
    context['title'] = game_session.title
