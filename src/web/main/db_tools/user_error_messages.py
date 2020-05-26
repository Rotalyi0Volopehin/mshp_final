class DBUserErrorMessages:
    """**Сообщения об ошибках, возникающих при работе в БД с данными о пользователях**\n
    Эти сообщения могут быть возвращены методами класса :class:`main.db_tools.user_tools.DBUserTools`
    при возникновении ошибок, о которых невозможно узнать, не проверяя пришедшие данные по БД.
    """
    login_is_already_in_use = "Пользователь с указанным логином уже существует!"
    email_is_already_in_use = "Пользователь с указанным E-mail уже существует!"
    invalid_user_configuration = "Некорректная конфигурация пользовательских данных!"
    not_found = "Пользователь не найден!"
    not_activated = "Пользователь не верифицирован!"
