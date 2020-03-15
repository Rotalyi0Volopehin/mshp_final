import json
import exceptions

from net_connection.core_classes import CoreClasses


# TODO: задокументировать


class CoreJSONEncoder(json.JSONEncoder):
    __default_json_serializable_types = [dict, list, str, int, float, bool, None]

    def default(self, obj):
        if type(obj) in CoreJSONEncoder.__default_json_serializable_types:
            return super().encode(obj)
        obj_module = obj.__module__
        obj_name = type(obj).__name__
        obj_dict = super().encode(obj.__dict__)
        encoded = "~$#{}.{}:{}".format(str(obj_module), str(obj_name), str(obj_dict))
        return encoded


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
        if CoreJSONDecoder.__is_encoded_core_object(decoded):
            return CoreJSONDecoder.__decode_core_object(decoded)
        if isinstance(decoded, list):
            for i in range(len(decoded)):
                item = decoded[i]
                if CoreJSONDecoder.__is_encoded_core_object(item):
                    decoded[i] = CoreJSONDecoder.__decode_core_object(item)
            return decoded
        if isinstance(decoded, dict):
            copy = {}
            for key, value in decoded.items():
                if CoreJSONDecoder.__is_encoded_core_object(key):
                    key = CoreJSONDecoder.__decode_core_object(key)
                if CoreJSONDecoder.__is_encoded_core_object(value):
                    value = CoreJSONDecoder.__decode_core_object(value)
                copy[key] = value
            return copy

    @staticmethod
    def __is_encoded_core_object(encoded):
        return isinstance(encoded, str) and encoded.startswith("~$#")

    @staticmethod
    def __decode_core_object(encoded: str):
        module_end = encoded.find('.', 3) - 1
        obj_module = encoded[3:module_end]
        class_origin = module_end + 2
        class_end = encoded.find(':', class_origin) - 1
        obj_class = encoded[class_origin:class_end]
        fields_origin = class_end + 2
        obj_fields = CoreJSONDecoder.decode_json(encoded[fields_origin:])
        return CoreClasses.classes[obj_module][obj_class](JSONInitTrojan(obj_fields))
