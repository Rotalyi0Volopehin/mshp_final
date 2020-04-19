#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


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


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_confrontation_web.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
