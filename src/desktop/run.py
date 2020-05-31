import pygame
import sys
import os


def fix_project_roots(*root_names):
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    src_path = current_path[:current_path.find("src") + 4]
    for root_name in root_names:
        sys.path.append(src_path + root_name)


try:
    import exceptions
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots("core")
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
