from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .menu import get_menu_context, get_user_menu_context
from main.models import GameSession
from main.db_tools.user_tools import DBUserTools
from main.db_tools.user_error_messages import DBUserErrorMessages
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.game_session_error_messages import DBGameSessionErrorMessages


@login_required
def join_gs_page(request, gsid):
    context = {
        "pagename": "Текущая сессия",
        "menu": get_menu_context(),
        "user_menu": get_user_menu_context(request.user)
    }
    ok, user_data, gs = get_data(request.user, gsid, context)
    if ok:
        context["title"] = gs.title
        context["level_limits"] = gs.level_limits_as_string
        context["players_gathered"] = gs.players_gathered
        if request.method == "POST":
            ok, error = DBUserParticipationTools.try_sign_user_up_for_session(request.user, gs)
            context["success"] = ok
            if not ok:
                context["error"] = error
    return render(request, "pages/join_session.html", context)


def get_data(user, gsid, context):
    ok, user_data = DBUserTools.is_user_configuration_correct(user, True)
    if not ok:
        context["error"] = DBUserErrorMessages.invalid_user_configuration
    else:
        ok = user_data.activated
        if not ok:
            context["error"] = DBUserErrorMessages.not_activated
        else:
            gs = GameSession.objects.filter(id=gsid)
            ok = len(gs) == 1
            if not ok:
                context["error"] = DBGameSessionErrorMessages.not_found
            else:
                return ok, user_data, gs[0]
    return ok, user_data, None
