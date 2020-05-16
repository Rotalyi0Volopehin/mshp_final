from django.contrib.auth import login as log_user_in, logout as log_user_out
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

import main.forms as forms
from main.db_tools.user_tools import DBUserTools
from main.views.form_view import FormView


class ProfileFormPage(FormView):
    """**View-класс страницы '/profile/<int:uid>/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """
    pagename = "Профиль"
    form_class = forms.ProfileForm
    template_name = "pages/profile/profile.html"

    @staticmethod
    def get_handler(context: dict, request, uid: int):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.get`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/profile/<int:uid>/'
        :type request: HttpRequest
        :param uid: ID пользователя, которому принадлежат данные профиля
        :type uid: int
        """
        user = ProfileFormPage.__get_user(uid)
        self = context["self"] = ProfileFormPage.__does_profile_belong_to_current_user(request.user, uid)
        ProfileFormPage.__try_pull_user_data_to_context(user, context, self)

    @staticmethod
    def post_handler(context: dict, request, form, uid: int):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.post`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/profile/<int:uid>/'
        :type request: HttpRequest
        :param form: форма, содержащая post-данные
        :type form: ProfileForm
        :param uid: ID пользователя, которому принадлежат данные профиля
        :type uid: int
        """
        self = context["self"] = ProfileFormPage.__does_profile_belong_to_current_user(request.user, uid)
        if not self:
            return HttpResponse(status_code=403)
        user = ProfileFormPage.__get_user(uid)
        ok, user_data = ProfileFormPage.__try_pull_user_data_to_context(user, context, self, return_user_data=True)
        if not ok:
            return
        action = form.data["action"]
        ProfileFormPage.__try_process_post_actions(action, context, form, user_data, user, request)
        if "del" in context:
            return redirect("/")

    @staticmethod
    def __get_user(uid: int) -> User:
        user, error = DBUserTools.try_find_user_with_id(uid)
        if user is None:
            raise Exception(error)
        return user

    @staticmethod
    def __does_profile_belong_to_current_user(req_user: User, uid: int) -> bool:
        return req_user.is_authenticated and (req_user.id == uid)

    @staticmethod
    def __try_pull_user_data_to_context(user: User, context: dict, self: bool, return_user_data=False):
        user_data, error = DBUserTools.try_get_user_data(user)
        if error is not None:
            context["ok"] = False
            context["error"] = error
            return False, None if return_user_data else False
        if self:
            context["pagename"] = "Мой профиль"
        context["login"] = user.username
        context["email"] = user.email
        context["regdate"] = user.date_joined
        context["victories"] = user_data.victories_count
        context["played_games"] = user_data.played_games_count
        context["activated"] = user_data.activated
        context["about"] = user_data.extra_info
        context["team"] = user_data.team
        context["exp"] = user_data.exp
        context["level"] = user_data.level
        context["reputation"] = user_data.reputation
        return True, user_data if return_user_data else True

    @staticmethod
    def __try_process_post_actions(action: str, context, form, user_data, user, request) -> bool:
        success = False
        error = None
        if action == "save-chan":  # сохранить изменения
            about = form.data["about"]
            user_data.extra_info = about
            user_data.save()
            success = True
        elif action == "save-pass":  # изменить пароль
            password = form.data["password"]
            if user.check_password(password):
                new_password = form.data["new_password"]
                if 0 < len(new_password) <= 64:
                    user.set_password(new_password)
                    user.save()
                    success = True
                    log_user_in(request, user)
                else:
                    error = "Длина пароля должна быть 1-64 символов!"
            else:
                error = "Текущий пароль не совпадает с указанным!"
        elif action == "del":  # удалить аккаунт
            log_user_out(request)
            DBUserTools.delete_user(user)
            context["del"] = success = True
        else:
            error = "Неверный формат отосланных данных!"
        context["ok"] = context["success"] = success
        context["error"] = error
        return success
