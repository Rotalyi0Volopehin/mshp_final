from django.db.models import Manager, QuerySet

import exceptions
from main.models import UserData


class DBUserTopTools:
    """**Инструменты получения топа пользователей из БД**
    """

    @staticmethod
    def get_top_by_level(count: int, top_base=UserData.objects) -> list:
        """**Инструмент получения топа пользователей по их уровню**\n
        Сортирует пользователей по убыванию их уровней, затем в рамках одного уровня по убыванию их опыта.\n
        Возвращаемый топ может иметь длину меньше count, если пользователей не хватает.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :param count: Желаемое количество пользователей в топе
        :type count: int
        :param top_base: Фрагмент БД, из которого составляется топ
        :type top_base: Manager или QuerySet
        :return: Топ пользователей
        :rtype: list
        """
        if not (isinstance(count, int) and (isinstance(top_base, Manager) or isinstance(top_base, QuerySet))):
            raise exceptions.ArgumentTypeException()
        ordered_by_level = top_base.order_by("-total_exp")[:count]
        return list(ordered_by_level)
