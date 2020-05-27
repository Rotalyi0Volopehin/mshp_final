import sys


def fix_project_roots(src_path, *root_names):
    """**Метод, исправляющий корни проекта**\n
    Вызывается из модулей :mod:`run.py` и :mod:`manage.py`, если корни проекта нарушены.

    Имена корней:\n
    - core
    - desktop
    - web

    :param src_path: Путь до директории 'src'
    :type src_path: str
    :param root_names: Имена корней, которые нужно подключить
    :type root_names: \\*args
    """
    for root_name in root_names:
        sys.path.insert(1, src_path + root_name)
