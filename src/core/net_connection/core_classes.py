import os
import importlib.util


# TODO: задокументировать


class CoreClasses:
    classes = {}

    @staticmethod
    def reg_core_classes():
        def file_handler(file_path):
            file_name = os.path.basename(file_path)
            if file_name.endswith(".py"):
                module_name = file_name[:-3]
                module = CoreClasses.__load_module(module_name, file_path)
                CoreClasses.classes[module_name] = CoreClasses.__get_classes_of_module(module)
        CoreClasses.__list_files("..", file_handler)

    @staticmethod
    def __list_files(dir_path, file_handler):
        for entry in os.listdir(dir_path):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                CoreClasses.__list_files(full_path, file_handler)
            else:
                file_handler(full_path)

    @staticmethod
    def __load_module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def __get_classes_of_module(module):
        classes = {}
        for name, elem in module.__dict__.items():
            if isinstance(elem, type):
                classes[name] = elem
        return classes
