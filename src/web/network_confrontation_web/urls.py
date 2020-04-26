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
from main.views import views, activation_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
from main.views.menu import get_menu_context, get_user_menu_context


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('activate/<str:uid>/<str:token>/', activation_view.activate, name='activate'),
    path('cad/', views.cad_page, name='cad'),
    path('darknet/', views.darknet_page, name='darknet'),
    path('forum/', views.forum_page, name='forum'),
    path('chat/', views.chat_page, name='chat'),
    path('profile/<int:uid>/', views.ProfileFormPage.as_view(), name='profile'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'menu': get_menu_context(),
                'usermenu': get_user_menu_context(AnonymousUser()),
                'pagename': 'Авторизация',
            }
        ),
        name='login'
    ),
    path('rating/', views.RatingFormPage.as_view(), name='rating'),
    path('registration/', views.RegistrationFormPage.as_view(), name='registration'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
