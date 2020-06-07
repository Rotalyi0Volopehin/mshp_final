"""
ASGI config for network_confrontation_web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import sys

from django.core.asgi import get_asgi_application


def fix_project_roots(*roots_names):
    """**Метод, исправляющий корни проекта**\n
    Вызывается из модуля :mod:`manage.py`, если корни проекта нарушены.

    Имена корней:\n
    - core
    - desktop
    - web

    :param roots_names: Имена корней, которые нужно подключить
    :type roots_names: \\*args
    """
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    src_path = current_path[:current_path.find("web")]
    for root_name in roots_names:
        sys.path.insert(0, src_path + root_name)


try:
    import exceptions
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots("core", "desktop")  # TODO: починить game_eng и удалить desktop из списка для патча
    import exceptions

    print("SUCCESS")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_confrontation_web.settings')

application = get_asgi_application()
