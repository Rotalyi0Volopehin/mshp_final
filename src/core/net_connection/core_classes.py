import os

from types import ModuleType


# TODO: задокументировать


class CoreClasses:
    classes = {}

    @staticmethod
    def reg_core_classes(core_dir_path):
        def file_handler(file_path):
            file_name = file_path[len(core_dir_path) + 1:]
            if file_name == "core_init.py":  # затычка для избежания рекурсии
                return
            if file_name.endswith(".py"):
                module_name = file_name[:-3].replace('\\', '.')
                module = CoreClasses.__load_module(module_name)
                CoreClasses.classes[module_name] = CoreClasses.__get_classes_of_module(module)
        CoreClasses.__list_files(core_dir_path, file_handler)

    @staticmethod
    def __load_module(name):
        module = __import__(name)
        while True:
            for elem in module.__dict__.values():
                if isinstance(elem, ModuleType):
                    module = elem
                    break
            return module

    @staticmethod
    def __list_files(dir_path, file_handler):
        for entry in os.listdir(dir_path):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                CoreClasses.__list_files(full_path, file_handler)
            else:
                file_handler(full_path)

    @staticmethod
    def __get_classes_of_module(module):
        classes = {}
        for name, elem in module.__dict__.items():
            if isinstance(elem, type):
                classes[name] = elem
        return classes