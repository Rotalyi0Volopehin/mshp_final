#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def fix_project_roots(*root_names):
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    src_path = current_path[:current_path.find("src") + 4]
    for root_name in root_names:
        sys.path.append(src_path + root_name)


try:
    # vvv этот импорт каким-то образом чинит один маленький баг; я не понимаю vvv
    from net_connection.core_classes import CoreClasses
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots("core")
    from net_connection.core_classes import CoreClasses
    print("SUCCESS")
del CoreClasses


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
