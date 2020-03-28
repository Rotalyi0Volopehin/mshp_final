import json
import exceptions

from net_connection.core_classes import CoreClasses
from enum import Enum


# TODO: задокументировать


class CoreJSONEncoder(json.JSONEncoder):
    __default_json_serializable_types = [dict, list, str, int, float, bool, None]

    def default(self, obj):
        if type(obj) in CoreJSONEncoder.__default_json_serializable_types:
            return super().encode(obj)
        if isinstance(obj, Enum):
            return CoreJSONEncoder.__encode_enum(obj)
        return CoreJSONEncoder.__encode_object_dict(obj)

    @staticmethod
    def __encode_object_dict(obj):
        obj_module, obj_type = CoreJSONEncoder.__get_info_module(obj)
        obj_dict = str(super().encode(obj.__dict__))
        encoded = "~$#{}.{}:{}".format(obj_module, obj_type, obj_dict)
        return encoded

    @staticmethod
    def __encode_enum(obj):
        obj_module, obj_type = CoreJSONEncoder.__get_info_module(obj)
        encoded = "~E#{}.{}:{}".format(obj_module, obj_type, obj.value)
        return encoded

    @staticmethod
    def __get_info_module(obj) -> (str, str):  # (obj_module, obj_type)
        obj_module = str(obj.__module__)
        obj_module = obj_module[obj_module.rfind('.') + 1:]
        obj_type = type(obj).__name__
        return obj_module, obj_type


class JSONInitTrojan:
    def __init__(self, fields: dict):
        if not isinstance(fields, dict):
            raise exceptions.ArgumentTypeException()
        self.fields = fields

    # decorator
    @staticmethod
    def json_init(init):
        if type(init).__name__ != "function":
            raise exceptions.ArgumentTypeException()

        def inner(*args, **kwargs):
            if (len(args) == 2) and (len(kwargs) == 0) and isinstance(args[1], JSONInitTrojan):
                self = args[0]
                trojan = args[1]
                self.__dict__.update(trojan.fields)
                return
            init(*args, **kwargs)
        return inner


class CoreJSONDecoder:
    @staticmethod
    def decode_json(json_: str):
        if not isinstance(json_, str):
            raise exceptions.ArgumentTypeException()
        decoded = json.loads(json_)
        success, obj = CoreJSONDecoder.__try_special_decoding(decoded)  # decode для str
        if success:
            return obj
        if isinstance(decoded, list):
            for i in range(len(decoded)):  # decode для list
                success, obj = CoreJSONDecoder.__try_special_decoding(decoded[i])
                if success:
                    decoded[i] = obj
            return decoded
        if isinstance(decoded, dict):  # decode для dict
            copy = {}
            for key, value in decoded.items():
                success, obj = CoreJSONDecoder.__try_special_decoding(key)
                if success:
                    key = obj
                success, obj = CoreJSONDecoder.__try_special_decoding(value)
                if success:
                    value = obj
                copy[key] = value
            return copy
        return decoded

    @staticmethod
    def __try_special_decoding(encoded) -> (bool, object):
        if isinstance(encoded, str):
            if encoded.startswith("~E#"):
                return True, CoreJSONDecoder.__decode_enum(encoded)
            if encoded.startswith("~$#"):
                return True, CoreJSONDecoder.__decode_core_object(encoded)
        return False, None

    @staticmethod
    def __is_encoded_core_object(encoded: str):
        return isinstance(encoded, str) and encoded.startswith("~$#")

    @staticmethod
    def __decode_enum(encoded: str):
        enum_type, enum_value = CoreJSONDecoder.__decode_object_info(encoded)
        enum = enum_type(enum_value)
        return enum

    @staticmethod
    def __decode_core_object(encoded: str):
        obj_type, obj_dict = CoreJSONDecoder.__decode_object_info(encoded)
        obj = obj_type(JSONInitTrojan(obj_dict))
        return obj

    @staticmethod
    def __decode_object_info(encoded: str) -> (type, str):  # (obj_type, obj_data)
        module_end = encoded.find('.', 3)
        obj_module_name = encoded[3:module_end]
        type_origin = module_end + 1
        type_end = encoded.find(':', type_origin)
        obj_type_name = encoded[type_origin:type_end]
        data_origin = type_end + 1
        obj_data = CoreJSONDecoder.decode_json(encoded[data_origin:])
        type_ = CoreClasses.classes[obj_module_name][obj_type_name]
        return type_, obj_data
