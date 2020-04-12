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
    project_path = os.path.abspath(".")
    src_path = os.path.join(project_path, "src")
    for root_name in roots_names:
        path = os.path.abspath(os.path.join(src_path, root_name))
        sys.path.insert(0, path)


try:
    from core_init import init_core
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots("core")
    from core_init import init_core
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
    init_core()
    main()
