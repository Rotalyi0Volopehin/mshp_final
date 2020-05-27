import pygame


# TODO: починить путь по-умолчанию при запуске run.py через консоль не из папки файла
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


def init_libs():
    pygame.mixer.init(22050, -16, 2, 64)
    pygame.display.init()
    pygame.font.init()


if __name__ == '__main__':
    init_libs()
    from game import Game
    g = Game()
    g.main_loop()
