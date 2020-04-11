def get_menu_context() -> list:
    """Генератор контекста навигационной панели

    :return: Контекст навигационной панели
    :rtype: list
    """
    return [
        {"url_name": "index", "name": "Главная"},
        {"url_name": "time", "name": "Текущее время"},
    ]
