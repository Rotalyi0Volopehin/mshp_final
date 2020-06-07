import exceptions

from game_eng.team import Team
# vvv импорты для чтения/записи vvv
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class Player:
    """**Модель игрока**
    """
    def __init__(self, uid: int, name: str, team: Team):
        if not (isinstance(uid, int) and isinstance(name, str) and isinstance(team, Team)):
            raise exceptions.ArgumentTypeException()
        self.id = uid
        self.name = name
        self.__team = team
        self.pressure_tools = dict()
        team.add_player(self)

    @staticmethod
    def read(stream: BinaryReader, game_model):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        uid = stream.read_uint()
        name = stream.read_short_string()
        team_ind = stream.read_sbyte()
        team = game_model.teams[team_ind]
        obj = Player(uid, name, team)
        game_model.player_ids[uid] = obj
        obj.read_pressure_tools(stream)
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, Player)):
            raise exceptions.ArgumentTypeException()
        stream.write_uint(obj.id)
        stream.write_short_string(obj.name)
        stream.write_sbyte(obj.team.index)
        obj.write_pressure_tools(stream)

    def read_pressure_tools(self, stream):
        for pts in stream.read_short_iterable(Player.get_pts_type(), {"player": self}):
            self.pressure_tools[type(pts)] = pts

    def write_pressure_tools(self, stream):
        stream.write_short_iterable(self.pressure_tools.values(), Player.get_pts_type())

    @property
    def team(self) -> Team:
        """**Фракция игрока**\n
        :return: Фракция
        :rtype: Team
        """
        return self.__team

    def add_pressure_tools(self, tool_type: type, count: int):
        """**Получение игроком некоторого количества ИВ одного типа**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises ArgumentValueException: |ArgumentValueException|
        :param tool_type: Тип ИВ
        :type tool_type: type
        :param count: Получаемое количество ИВ (>= 0)
        :type count: int
        """
        if not (isinstance(tool_type, type) and isinstance(count, int)):
            raise exceptions.ArgumentTypeException()
        if not issubclass(tool_type, Player.get_pts_type()) or (count < 0):
            raise exceptions.ArgumentValueException()
        if tool_type in self.pressure_tools:
            self.pressure_tools[tool_type].count += count
            return
        pt_set = tool_type(self)
        self.pressure_tools[tool_type] = pt_set
        pt_set.count = count

    @staticmethod  # костыль для избежания циклического импорта
    def get_pts_type() -> type:
        if not hasattr(Player, "__pts_type"):
            from game_eng.pressure_tool_set import PressureToolSet
            Player.__pts_type = PressureToolSet
        return Player.__pts_type
