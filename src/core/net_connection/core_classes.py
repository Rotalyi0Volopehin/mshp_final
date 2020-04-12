import os


# TODO: задокументировать


class CoreClasses:
    classes = {}

    @staticmethod
    def reg_core_classes(core_dir_path):
        def file_handler(file_path):
            file_name = file_path[len(core_dir_path) + 1:]
            if file_name.endswith(".py") and not file_name.endswith("__init__.py"):
                module_name = file_name[:-3].replace(os.path.sep, '.')
                module = CoreClasses.__load_module(module_name)
                CoreClasses.classes[module_name] = CoreClasses.__get_classes_of_module(module)
        CoreClasses.__list_files(core_dir_path, file_handler)

    @staticmethod
    def __load_module(name):
        module = __import__(name)
        name_segs = name.split('.')[1:]
        for name_seg in name_segs:
            module = module.__dict__[name_seg]
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
