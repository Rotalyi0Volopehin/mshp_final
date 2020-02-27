import importlib.util
import exceptions


# TODO: задокументировать код


#   Пример использования:
# import main.external_modules as em
# import os
# constants_path = os.path.join("..", "adventures_desktop", "constants.py")  # ../adventures_desktop/constants.py
# constants = em.load_module("constants", constants_path)
# print(constants.Color.RED)  # OUTPUT: (255, 0, 0)


__modules = {}  # Подгруженные модули


def load_module(name, path):  # Загружает и возвращает модуль
    if not (isinstance(name, str) and isinstance(path, str)):
        raise exceptions.ArgumentTypeException
    if name in __modules:
        module = __modules[name]
    else:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        __modules[name] = module
    return module
