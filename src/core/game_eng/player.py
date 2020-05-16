import exceptions

from game_eng.team import Team


class Player:
    """**Модель игрока**
    """
    def __init__(self, name: str, team: Team):
        if not (isinstance(name, str) and isinstance(team, Team)):
            raise exceptions.ArgumentTypeException()
        self.name = name
        self.__team = team
        self.pressure_tools = dict()

    @property
    def team(self) -> Team:
        """**Фракция игрока**\n
        :return: Фракция
        :rtype: Team
        """
        return self.__team

    def add_pressure_tools(self, tool_type: type, count: int):
        """**Получение игроком некоторого количества ИВ одного типа**\n
        :raises ArgumentTypeException: Неверный тип переданных аргументов
        :raises ArgumentValueException: Значение переданных аргументов не соответсвует требованиям
        :param tool_type: Тип ИВ
        :type tool_type: type
        :param count: Получаемое количество ИВ (>= 0)
        :type count: int
        """
        if not (isinstance(tool_type, type) and isinstance(count, int)):
            raise exceptions.ArgumentTypeException()
        if not issubclass(tool_type, self.pts_type) or (count < 0):
            raise exceptions.ArgumentValueException()
        if tool_type in self.pressure_tools:
            self.pressure_tools[tool_type].count += count
            return
        pt_set = tool_type(self)
        self.pressure_tools[tool_type] = pt_set
        pt_set.count = count

    @property  # костыль для избежания циклического импорта
    def pts_type(self) -> type:
        if not hasattr(Team, "__pts_type"):
            from game_eng.pressure_tool_set import PressureToolSet
            Player.__pts_type = PressureToolSet
        return Player.__pts_type
