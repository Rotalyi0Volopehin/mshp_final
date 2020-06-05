from main.forms import CreateSessionForm
from main.views.form_view import FormView
from main.db_tools.user_tools import DBUserTools
from main.db_tools.user_error_messages import DBUserErrorMessages
from main.db_tools.game_session_tools import DBGameSessionTools


class CreateSessionFormPage(FormView):
    pagename = "Создание сессии"
    form_class = CreateSessionForm
    template_name = "pages/create_session.html"
    login_required = True
    invalid_form_error = False

    @staticmethod
    def post_handler(context: dict, request, form: CreateSessionForm):
        ok, user_data = DBUserTools.is_user_configuration_correct(request.user, True)
        if not ok:
            raise Exception(DBUserErrorMessages.invalid_user_configuration)
        if not user_data.activated:
            raise Exception(DBUserErrorMessages.not_activated)
        title = form.data["session_name"]
        player_per_team = int(form.data["user_per_team"])
        player_turn_period = int(form.data["turn_period"])
        team_money_limit = int(form.data["money_limit"])
        min_level_limited = "min_level_limit_existence" in form.data
        max_level_limited = "max_level_limit_existence" in form.data
        #min_level_limited = form.data["min_level_limit_existence"] == "true"
        #max_level_limited = form.data["max_level_limit_existence"] == "true"
        min_level = int(form.data["user_min_level"]) if min_level_limited else -1
        max_level = int(form.data["user_max_level"]) if max_level_limited else 0xFFFF
        gs, error = DBGameSessionTools.try_create_new_session(title, player_turn_period, player_per_team,
                                                              team_money_limit, min_level, max_level)
        if gs is None:
            raise Exception(error)
        context["success"] = True
