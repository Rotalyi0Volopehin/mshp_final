from main.forms import CurrentSessionForm
from main.views.form_view import FormView
from main.db_tools.user_tools import DBUserTools
from main.db_tools.user_error_messages import DBUserErrorMessages
from main.db_tools.game_session_tools import DBGameSessionTools


class CreateSessionFormPage(FormView):
    pagename = "Текущая сессия"
    form_class = CurrentSessionForm
    template_name = "pages/current_session.html"
    login_required = True
    invalid_form_error = False

    @staticmethod
    def post_handler(context: dict, request, form: CurrentSessionForm):
        ok, user_data = DBUserTools.is_user_configuration_correct(request.user, True)
        if not ok:
            raise Exception(DBUserErrorMessages.invalid_user_configuration)
        if not user_data.activated:
            raise Exception(DBUserErrorMessages.not_activated)
        title = "Название"
        user_level = "уровни"
        user_fill = "Заполненность сессии"
        create_date = "12.04.2020 16:87"
        context["success"] = True
