from django.contrib.auth.decorators import login_required

from main.views.menu import get_menu_context, get_user_menu_context
from django.shortcuts import render
from main.models import UserData
from main.models import UserParticipation
from main.models import GameSession
from main.db_tools.game_session_tools import DBGameSessionTools
from main.db_tools.user_tools import DBUserTools


@login_required
def game_session_page(request):
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
        participation = UserParticipation.objects.filter(user_data=user_data)
        if participation.count() == 0:
            context['state'] = 0
        elif participation[0].game_session.phase == 0:
            context['state'] = 1
            expectation_game_session_state(context, participation[0].game_session)
        else:
            context['state'] = 2
            playing_game_session_state(context, participation[0].game_session, user_data)
    context['state'] = 2
    return render(request, 'pages/current_session/game_session_body.html', context)


def expectation_game_session_state(context, game_session):
    add_game_session_name_to_context(context, game_session)
    participations = UserParticipation.objects.filter(game_session=game_session)
    context['player_count'] = len(participations)
    context['players_must_be'] = game_session.user_per_team_count * 3


def playing_game_session_state(context, game_session, user_data):
    add_game_session_name_to_context(context, game_session)
    participants = ([], [], [])
    participations = UserParticipation.objects.filter(game_session=game_session)
    for participation in participations:
        name = participation.user_data.user.username
        self = participation.user_data == user_data
        participants[participation.user_data.team].append((name, self))
    context['players'] = participants
    # TODO: передать ссылки на чаты


def add_game_session_name_to_context(context, game_session):
    context['session_name'] = game_session.title
