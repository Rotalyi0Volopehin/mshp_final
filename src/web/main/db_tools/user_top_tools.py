import exceptions

from main.models import UserData
from django.db.models import Manager, QuerySet


class DBUserTopTools:
    """**Инструменты получения топа пользователей из БД**
    """
    @staticmethod
    def get_top_by_level(count: int, top_base=UserData.objects) -> list:
        """**Инструмент получения топа пользователей по их уровню**\n
        Сортирует пользователей по убыванию их уровней, затем в рамках одного уровня по убыванию их опыта.\n
        Возвращаемый топ может иметь длину меньше count, если пользователей не хватает.

        :raises ArgumentTypeException: Неверный тип переданных аргументов
        :param count: Желаемое количество пользователей в топе
        :type count: int
        :param top_base: Фрагмент БД, из которого составляется топ
        :type top_base: Manager или QuerySet
        :return: Топ пользователей
        :rtype: list
        """
        if not (isinstance(count, int) and (isinstance(top_base, Manager) or isinstance(top_base, QuerySet))):
            raise exceptions.ArgumentTypeException()
        ordered_by_level = top_base.order_by("-level")[:count]
        if len(ordered_by_level) < count:
            sorted(ordered_by_level, key=lambda user_data: user_data.exp)
            return list(ordered_by_level)
        border_user = ordered_by_level[count - 1]
        border_users = top_base.filter(level=border_user.level).order_by("-level")
        border_origin = 0
        for i in range(count - 2, -1, -1):
            if ordered_by_level[i].level > border_user.level:
                border_origin = count - i + 1
                break
        ordered_twice = []
        for i in range(count):
            ordered_twice.append(ordered_by_level[i] if i < border_origin else border_users[i - border_origin])
        return ordered_twice
