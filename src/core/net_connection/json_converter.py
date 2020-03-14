import json
import exceptions


# TODO: задокументировать


class JSONInitTrojan:
    def __init__(self, json_):
        if not isinstance(json_, str):
            raise exceptions.ArgumentTypeException()
        self.__json = json_

    @property
    def json(self):
        return self.__json


class JSONConverter:
    @staticmethod
    def object_to_json(obj) -> str:
        return json.dumps(obj.__dict__)

    @staticmethod
    def object_from_json(json_, obj):
        obj.__dict__.update(json.loads(json_))
        return obj

    # decorator
    @staticmethod
    def json_init(init):
        if str(type(init)) != "<class 'function'>":
            raise exceptions.ArgumentTypeException()
        def inner(*args, **kwargs):
            if (len(args) == 2) and (len(kwargs) == 0) and isinstance(args[1], JSONInitTrojan):
                self = args[0]
                trojan = args[1]
                JSONConverter.object_from_json(trojan.json, self)
                return
            init(*args, **kwargs)
        return inner
