import main.forms as forms

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import UserParticipation
from main.db_tools.user_participation_tools import DBUSerParticipationTools
from main.views.form_view import FormView
from main.views.menu import get_user_menu_context


class SessionsFormPage(FormView):
    """**View-класс страницы '/registration/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """
    pagename = "Поиск сессии"
    form_class = forms.SessionsForm
    template_name = "pages/sessions.html"
    ROWS_PER_PAGE = 8

    @staticmethod
    def get_handler(context: dict, request):
        """**Дополнительный обработчик get-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.get`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/sessions/'
        :type request: HttpRequest
        """
        page_ind = int(request.GET.get("page", "0"))
        session_offset = page_ind * SessionsFormPage.ROWS_PER_PAGE
        sessions, error = DBUSerParticipationTools.search_sessions_for_user_participation(request.user)
        if error is not None:
            raise Exception(error)
        page_count = len(sessions) // SessionsFormPage.ROWS_PER_PAGE
        if len(sessions) % SessionsFormPage.ROWS_PER_PAGE > 0:
            page_count += 1
        context["cant_back"] = page_ind <= 0
        context["cant_forward"] = page_ind >= page_count
        context["page"] = page_ind + 1
        context["prev_page"] = page_ind - 1
        context["next_page"] = page_ind + 1
        context["page_count"] = page_count
        context["table"] = table = list()
        for i in range(SessionsFormPage.ROWS_PER_PAGE):
            if i == len(sessions):
                break
            session = sessions[i + session_offset]
            table.append(SessionsFormPage.__get_session_table_row(session))
        context["ok"] = True

    @staticmethod
    def __get_session_table_row(session) -> tuple:
        level_limits = ""
        if session.user_lowest_level != -1:
            level_limits += f"от {session.user_lowest_level} "
        if session.user_highest_level != -1:
            level_limits += f"до {session.user_highest_level}"
        participant_count = len(UserParticipation.objects.filter(game_session=session))
        participant_required = session.user_per_team_count * 3
        player_count = f"{participant_count} из {participant_required}"
        return session, level_limits, player_count
