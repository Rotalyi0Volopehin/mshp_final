"""
WSGI config for network_confrontation_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


def fix_project_roots(*root_names):
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    src_path = current_path[:current_path.find("src") + 4]
    for root_name in root_names:
        sys.path.append(src_path + root_name)


try:
    from net_connection.core_classes import CoreClasses
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots("core")
    from net_connection.core_classes import CoreClasses

    print("SUCCESS")
del CoreClasses

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_confrontation_web.settings')

application = get_wsgi_application()
