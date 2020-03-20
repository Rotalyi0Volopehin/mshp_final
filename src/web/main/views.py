import datetime

from django.contrib.auth.decorators import login_required

import main.forms
from django.shortcuts import render, redirect
from main.db_tools.user_tools import DBUserTools
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login, logout

def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'darknet', 'name': 'DarkNet'},
        {'url_name': 'forum', 'name': 'Форум'},
        {'url_name': 'chat', 'name': 'Закрытые каналы'},

    ]

def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)

def view_func_template(request, html_path, form_class, post_handler, get_handler=None, context=None):
    if context is None:
        context = {}
    context["menu"] = get_menu_context()
    success = ok = False
    error = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            ok, error, success = post_handler(form=form, context=context)
        else:
            error = "Неверный формат отосланных данных!"
    else:
        if get_handler is None:
            form = form_class()
            ok = True
        else:
            ok, error, success, form = get_handler(context=context)
    context["form"] = form
    context["ok"] = ok
    context["error"] = error
    context["success"] = success
    return render(request, html_path, context)

def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context()
    }
    return render(request, 'pages/darknet.html', context)


def forum_page(request):
    context = {
        'pagename': 'Форум',
        'menu': get_menu_context()
    }
    return render(request, 'pages/forum.html', context)


def chat_page(request):
    context = {
        'pagename': 'Закрытые каналы',
        'menu': get_menu_context()
    }
    return render(request, 'pages/chat.html', context)


def registration_page(request):  #затычка для проверки бд
    context = {"pagename": "Регистрация"}
    def post_handler(form, context) -> (bool, str, bool):
        password = form.data["password1"]
        login_ = form.data["login"]
        ok, error = DBUserTools.try_register(login_, password, form.data["email"], form.data['team'])
        return ok, error, ok
    return view_func_template(request, "registration/registration.html", main.forms.RegistrationForm, post_handler, context=context)


def profile_page(request, id):
    context = {}
    def body(form=None, context=None):
        ok = success = False
        user, error = DBUserTools.try_find_user_with_id(id)
        if error is None:
            user_data, error = DBUserTools.try_get_user_data(user)
            if error is None:
                self = context['self'] = not isinstance(request.user, AnonymousUser) and (user.id == request.user.id)
                context['pagename'] = "Мой профиль" if self else "Профиль"
                if self and (form != None):
                    ok, error, success = post_handler(form, context, user, user_data)
                context['login'] = user.username
                #context['name'] = user.first_name
                context['email'] = user.email
                context['regdate'] = user.date_joined
                context['victories'] = user_data.victories_count
                context['played_games'] = user_data.played_games_count
                context['activated'] = user_data.activated
                context['about'] = user_data.extra_info
                context['team'] = user_data.team
                context['exp'] = user_data.exp
        else:
            context["pagename"] = "Профиль"
        result = [ok, error, success]
        if form is None:
            result.append(None)
        return result
    def post_handler(form, context, user, user_data):
        success = ferr = False
        error = None
        action = form.data["action"]
        if action == "save-chan":
            name = form.data["login"]
            if 0 < len(name) <= 64:
                about = form.data["about"]
                #user.first_name = name
                #user.save()
                user_data.extra_info = about
                user_data.save()
                success = True
            else:
                ferr = True
        elif action == "save-pass":
            password = form.data["password"]
            if user.check_password(password):
                new_password = form.data["new_password"]
                if 0 < len(new_password) <= 64:
                    user.set_password(new_password)
                    user.save()
                    success = True
                else:
                    error = "Длина пароля должна быть больше 1, но меньше 65 символов!"
            else:
                error = "Текущий пароль не совпадает с указанным!"
        elif action == "del":
            logout(request)
            user.delete()
            context["del"] = success = True
        else:
            ferr = True
        if ferr:
            error = "Неверный формат отосланных данных!"
        return success, error, success
    result = view_func_template(request, "pages/profile.html", main.forms.ProfileForm, body, get_handler=body, context=context)
    return redirect("/") if "del" in context else result

@login_required
def my_profile_page(request):
    return profile_page(request, request.user.id)