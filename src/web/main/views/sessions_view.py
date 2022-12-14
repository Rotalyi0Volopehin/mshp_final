""" View функции страницы сессий """

from main.models import GameSession
from main.db_tools.user_tools import DBUserTools
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.game_session_tools import DBGameSessionTools
from main.views.form_view import FormView
import main.forms as forms


class SessionsFormPage(FormView):
    """**View-класс страницы '/registration/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """
    pagename = "Поиск сессии"
    form_class = forms.SessionsForm
    template_name = "pages/sessions.html"
    login_required = True
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
        sessions, error = DBUserParticipationTools.search_sessions_for_user_participation\
            (request.user)
        if error is not None:
            raise Exception(error)
        page_count = len(sessions) // SessionsFormPage.ROWS_PER_PAGE
        if len(sessions) % SessionsFormPage.ROWS_PER_PAGE > 0:
            page_count += 1
        SessionsFormPage.__put_page_info_into_context(context, page_ind, page_count)
        context["table"] = table = list()
        for i in range(SessionsFormPage.ROWS_PER_PAGE):
            if i == len(sessions):
                break
            session = sessions[i + session_offset]
            table.append(SessionsFormPage.__get_session_table_row(session))
        context["ok"] = True

    @staticmethod
    def __get_session_table_row(session) -> tuple:
        """**Получение строки сессии для таблицы**

        :param session: игровая сессия
        :type session: GameSession
        :return: строка сессии для талицы
        :rtype: tuple
        """
        return session, session.level_limits_as_string, session.players_gathered

    @staticmethod
    def __put_page_info_into_context(context: dict, page_ind: int, page_count: int):
        """**Установка информации о страницы в context**

        :param context: context страницы
        :type context: dict
        :param page_ind: идентификатор страницы
        :type page_ind: int
        :param page_count: количество страниц
        :type page_count: int
        """
        context["nothing_found"] = page_count == 0
        context["cant_back"] = page_ind <= 0
        context["cant_forward"] = page_ind >= page_count - 1
        context["page"] = page_ind + 1
        context["prev_page"] = page_ind - 1
        context["next_page"] = page_ind + 1
        context["page_count"] = page_count

    @staticmethod
    def post_handler(context: dict, request, form):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.post`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/sessions/'
        :type request: HttpRequest
        :param form: форма, содержащая post-данные
        :type form: SessionsForm
        """
        session_title = form.data["session_title"]
        if len(session_title) == 0:
            return SessionsFormPage.get_handler(context, request)
        session = GameSession.objects.filter(title=session_title)
        session = None if len(session) == 0 else session[0]
        context["table"] = table = list()
        page_count = 0
        if session is not None:
            user_data, error = DBUserTools.try_get_user_data(request.user)
            if error is not None:
                raise Exception(error)
            participation_possibility, error =\
                DBGameSessionTools.can_user_take_part_in_session(request.user, user_data, session)
            if error is not None:
                raise Exception(error)
            if participation_possibility:
                table.append(SessionsFormPage.__get_session_table_row(session))
                page_count = 1
        SessionsFormPage.__put_page_info_into_context(context, 0, page_count)
