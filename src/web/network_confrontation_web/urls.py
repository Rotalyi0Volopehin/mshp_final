"""network_confrontation_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import views, activation_view, chat
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
from main.views.menu import get_menu_context, get_user_menu_context

from main.views import profile_view, registration_view, fractions_view, sessions_view
from main.views import views, activation_view, darknet_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('activate/<str:uid>/<str:token>/', activation_view.activate, name='activate'),
    path('cad/', views.cad_page, name='cad'),
    path('darknet/', darknet_view.darknet_page, name='darknet'),
    path('forum/', views.forum_page, name='forum'),
    path('sessions/', sessions_view.SessionsFormPage.as_view(), name='sessions'),
    path('profile/<int:uid>/', profile_view.ProfileFormPage.as_view(), name='profile'),
    path('fraction0/', fractions_view.FractionPages.fraction0_page, name='fraction0'),
    path('fraction1/', fractions_view.FractionPages.fraction1_page, name='fraction1'),
    path('fraction2/', fractions_view.FractionPages.fraction2_page, name='fraction2'),
    path('login/', views.LoginFormPage.as_view(), name='login'),
    path('registration/', registration_view.RegistrationFormPage.as_view(), name='registration'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('chat/room/<str:room_name>/', chat.room, name='chat_room'),
    path('chat/user/<int:user_id>/', chat.open_user_chat, name='chat_open_user'),
    path('chat/list/', chat.chats_list, name='chat'),
]
