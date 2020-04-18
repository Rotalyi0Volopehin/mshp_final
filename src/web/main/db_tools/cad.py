from main import models
from django.contrib.auth.models import User
from django.db.models import Model


class CAD:
    """**Класс, чистящий все таблицы**
    """
    @staticmethod
    def clear_all_data():
        """**Инструмент стирания данных из всех таблиц**\n
        \\* всех таблиц, модели которых прописаниы в модуле :mod:`main.models`, а также таблицы модели User
        """
        CAD.__clear_table(User)
        for _, elem in models.__dict__.items():
            if isinstance(elem, type) and issubclass(elem, Model):
                CAD.__clear_table(elem)

    @staticmethod
    def __clear_table(model):
        model.objects.all().delete()
