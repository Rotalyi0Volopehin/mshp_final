import os
import exceptions

from .hash_algos import HashAlgos
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class CoreClasses:
    classes = {}

    @staticmethod
    def reg_core_classes(core_dir_path: str):
        def file_handler(file_path):
            file_name = file_path[len(core_dir_path) + 1:]
            if file_name.endswith(".py") and not file_name.endswith("__init__.py"):
                module_name = file_name[:-3].replace(os.path.sep, '.')
                module = CoreClasses.__load_module(module_name)
                module_hash = HashAlgos.hash_str(module_name)
                existing_same_module = CoreClasses.classes.get(module_hash, None)
                if existing_same_module is not None:
                    if existing_same_module == module:
                        print(f"Module '{module.__name__}' is seen twice. Ignoring")
                    else:
                        raise exceptions.CoreModuleHashOverlapException()
                else:
                    CoreClasses.classes[module_hash] = CoreClasses.__get_classes_of_module(module)
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
                class_hash = HashAlgos.hash_str(name)
                if class_hash in classes:
                    raise exceptions.CoreClassHashOverlapException()
                classes[class_hash] = elem
        return classes

    @staticmethod
    def read_class(stream: BinaryReader) -> type:
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        module_hash = stream.read_uint()
        class_hash = stream.read_uint()
        return CoreClasses.classes[module_hash][class_hash]

    @staticmethod
    def write_class(stream: BinaryWriter, cls: type):
        if not (isinstance(stream, BinaryWriter) and isinstance(cls, type)):
            raise exceptions.ArgumentTypeException()
        if isinstance(None, cls):
            raise Exception("NoneType is not supported!")
        stream.write_uint(HashAlgos.hash_str(cls.__module__))
        stream.write_uint(HashAlgos.hash_str(cls.__name__))
