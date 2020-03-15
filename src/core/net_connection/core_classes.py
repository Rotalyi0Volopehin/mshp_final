import os
import importlib.util


core_classes = {}


def reg_core_classes():
    def file_handler(file_path):
        file_name = os.path.basename(file_path)
        if file_name == "core_classes.py":  # TODO: добавить init
            return
        if file_name.endswith(".py"):
            module_name = file_name[:-3]
            module = load_module(module_name, file_path)
            core_classes[module_name] = get_classes_of_module(module)
    list_files("..", file_handler)


def list_files(dir_path, file_handler):
    for entry in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            list_files(full_path, file_handler)
        else:
            file_handler(full_path)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_classes_of_module(module):
    classes = {}
    for name, elem in module.__dict__.items():
        if isinstance(elem, type):
            classes[name] = elem
    return classes


reg_core_classes()
