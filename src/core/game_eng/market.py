import exceptions
import math
import os

from types import ModuleType
from game_eng.pressure_tool_set import PressureToolSet
from game_eng.player import Player
# vvv импорты для чтения/записи vvv
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class Market:
    """**Модель Даркнета**\n
    Иммитирует рынок ИВ.\n
    Статические поля:\n
    - tool_types (*set of PressureToolSet*) - ИВ, которые могут быть куплены в Даркнете
    """
    @staticmethod
    def collect_tool_types():
        """**Сбор всех ИВ, которые могут быть куплены в Даркнете**\n
        Собирает в поле 'Market.tool_types' все классы, содержащиеся в модулях директории 'pressure_tool_set_ders',
        отнаследованные от класса :cls:`game_eng.pressure_tool_set.PressureToolSet` и
        имеющие статическое поле '__END_PRODUCT__'.\n
        Запускается автоматически при инициализации модуля.
        """
        Market.tool_types = set()
        root_path = os.path.abspath(os.path.dirname(exceptions.__file__))
        pts_ders_dir = os.path.join(root_path, "game_eng", "pressure_tool_set_ders")
        for entry in os.listdir(pts_ders_dir):
            if entry.endswith(".py") and (entry != "__init__.py"):
                module_name = f"game_eng.pressure_tool_set_ders.{entry[:len(entry) - 3]}"
                module = Market.__load_module(module_name)
                Market.__reg_pts_of_module(module)

    @staticmethod
    def __load_module(name):
        module = __import__(name)
        name_segs = name.split('.')[1:]
        for name_seg in name_segs:
            module = module.__dict__[name_seg]
        return module

    @staticmethod
    def __reg_pts_of_module(module: ModuleType):
        for type_ in module.__dict__.values():
            if isinstance(type_, type) and issubclass(type_, PressureToolSet) and hasattr(type_, "__END_PRODUCT__"):
                Market.tool_types.add(type_)

    @staticmethod
    def read(stream: BinaryReader):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        obj = Market()
        for slot in stream.read_short_iterable(MarketSlot):
            obj.assortment[type(slot.pt_set)] = slot
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, Market)):
            raise exceptions.ArgumentTypeException()
        stream.write_short_iterable(obj.assortment.values(), MarketSlot)

    def __init__(self):
        self.assortment = {}
        for tool_type in Market.tool_types:
            tool = tool_type()
            self.assortment[tool_type] = MarketSlot(tool, tool.production_cost << 1)

    def try_buy(self, buyer: Player, tool_type: type, count: int) -> bool:
        """**Попытка покупки игроком нескольких ИВ одного типа**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises ArgumentValueException: |ArgumentValueException|
        :param buyer: Покупатель
        :type buyer: Player
        :param tool_type: Тип ИВ
        :type tool_type: type
        :param count: Требуемое количество (>= 0)
        :type count: int
        :return: ok
        :rtype: bool
        """
        # vvv проверка аргументов vvv
        if not (isinstance(buyer, Player) and isinstance(tool_type, type) and isinstance(count, int)):
            raise exceptions.ArgumentTypeException()
        if count < 0:
            raise exceptions.ArgumentValueException()
        if tool_type not in self.assortment:
            raise exceptions.ArgumentValueException("Argument 'tool_type' is not contained in 'assortment' as a key!")
        # vvv проверка возможности vvv
        slot = self.assortment[tool_type]
        if slot.pt_set.count < count:
            return False
        total_price = count * slot.price
        if buyer.team.money < total_price:
            return False
        # vvv выполнение покупки vvv
        buyer.add_pressure_tools(tool_type, count)
        buyer.team.money -= total_price
        slot.pt_set.count -= count
        return True

    def update(self):
        """**Обновление ассортимента**\n
        Пополняет ассортимент ИВ, при этом происходит изменение цен и количества ИВ определённых типов.\n
        Выполняется при окончании хода любой фракции.
        """
        for slot in self.assortment.values():
            slot.update_price_and_count()
            slot.refresh_count()


class MarketSlot:
    """**Слот Даркнета с однотипными товарами**
    """
    def __init__(self, pt_set, price):
        self.pt_set = pt_set
        self.price = price
        self.start_count = pt_set.count

    @staticmethod
    def read(stream: BinaryReader):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        pt_set = PressureToolSet.read(stream)
        price = stream.read_uint()
        obj = MarketSlot(pt_set, price)
        obj.start_count = stream.read_uint()
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, MarketSlot)):
            raise exceptions.ArgumentTypeException()
        PressureToolSet.write(stream, obj.pt_set)
        stream.write_uint(obj.price)
        stream.write_uint(obj.start_count)

    def update_price_and_count(self):
        """**Обновление цены и количества ИВ этого типа**\n
        Изменения зависят от спроса.
        """
        sold_ratio = self.pt_set.count / self.start_count
        if sold_ratio == 0.0:
            self.start_count += MarketSlot.__calc_dynamic_value_delta(self.start_count)
            overprice = self.price - self.pt_set.production_cost
            overprice += MarketSlot.__calc_dynamic_value_delta(overprice)
            self.price = overprice + self.pt_set.production_cost
        elif sold_ratio >= 0.25:
            if self.start_count > 1:
                self.start_count -= MarketSlot.__calc_dynamic_value_delta(self.start_count)
            overprice = self.price - self.pt_set.production_cost
            if overprice > 0:
                overprice -= MarketSlot.__calc_dynamic_value_delta(overprice)
                self.price = overprice + self.pt_set.production_cost

    @staticmethod
    def __calc_dynamic_value_delta(count: int) -> int:
        return 1 if count < 4 else int(math.log2(count))

    def refresh_count(self):
        """**Пополнение количества ИВ**
        """
        if self.pt_set.count < self.start_count:
            self.pt_set.count = self.start_count


Market.collect_tool_types()
