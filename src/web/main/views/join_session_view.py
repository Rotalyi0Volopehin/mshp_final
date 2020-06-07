""" Страница подключения к сессии """

from main.db_tools.game_session_error_messages import DBGameSessionErrorMessages
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.user_error_messages import DBUserErrorMessages
from main.db_tools.user_tools import DBUserTools
from main.models import GameSession

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .menu import get_menu_context, get_user_menu_context


@login_required
def join_gs_page(request, gsid):
    """**View-функция страницы подключения к сессии**

    :param request: request на страницу подключения к сессии
    :type request: HttpRequest
    :param gsid: ID сессии
    :type gsid: int
    :return: response
    :rtype: HttpResponse
    """
    context = {
        "pagename": "Текущая сессия",
        "menu": get_menu_context(),
        "user_menu": get_user_menu_context(request.user)
    }
    status_result, user_data, game_session = get_data(request.user, gsid, context)
    if status_result:
        context["title"] = game_session.title
        context["level_limits"] = game_session.level_limits_as_string
        context["players_gathered"] = game_session.players_gathered
        if request.method == "POST":
            status_result, error = DBUserParticipationTools.try_sign_user_up_for_session(
                request.user,
                game_session
            )
            context["success"] = status_result
            if not status_result:
                context["error"] = error
    return render(request, "pages/join_session.html", context)


def get_data(user, gsid, context):
    """**Получение данных страницы**

    :param user: пользователь
    :type user: User
    :param gsid: ID сессии
    :type gsid: int
    :param context: контекст страницы
    :type context: dict
    :return: данные страницы
    :rtype: tuple
    """
    status_result, user_data = DBUserTools.is_user_configuration_correct(user, True)
    if not status_result:
        context["error"] = DBUserErrorMessages.invalid_user_configuration
    else:
        status_result = user_data.activated
        if not status_result:
            context["error"] = DBUserErrorMessages.not_activated
        else:
            game_session = GameSession.objects.filter(id=gsid)
            status_result = len(game_session) == 1
            if not status_result:
                context["error"] = DBGameSessionErrorMessages.not_found
            else:
                return status_result, user_data, game_session[0]
    return status_result, user_data, None
