#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def fix_project_roots():
    import importlib.util as imp
    import sys
    import os
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    src_path = current_path[:current_path.find("src") + 4]
    root_patcher_path = os.path.join(src_path, "core", "root_patcher.py")
    spec = imp.spec_from_file_location("root_patcher", root_patcher_path)
    root_patcher = imp.module_from_spec(spec)
    spec.loader.exec_module(root_patcher)
    root_patcher.fix_project_roots(src_path, "core")


try:
    import exceptions
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots()
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
