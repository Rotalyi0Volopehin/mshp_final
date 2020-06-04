"""adventures_web URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from main import views
from django.contrib.auth import views as auth_views

from main.views import get_menu_context

urlpatterns = [
    path('dialogs/', login_required(views.DialogsView.as_view()), name='dialogs'),
    path('dialogs/create/<int:user_id>/', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    path('dialogs/<int:chat_id>/', login_required(views.MessagesView.as_view()), name='messages'),
    path('', include('permalinks.urls')),
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('darknet/', views.darknet_page, name='darknet'),
    path('forum/', views.forum_page, name='forum'),
    path('chat/', views.chat_page, name='chat'),
    path('profile/', views.profile_page, name='profile'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'menu': get_menu_context(),
                'pagename': 'Авторизация'
            }
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
