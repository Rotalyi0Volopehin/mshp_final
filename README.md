# Проект "Network Confrontation"

### Цель

Игра в desktop'е; развитие - в web'е

### Технологический стек:

- python 3.6
- django 3.0+
- sqlite 3.22+
- pygame 1.9.6+

### Инструкция по настройке проекта:

1. Склонировать проект
```bash
git clone https://gitlab.informatics.ru/2019-2020/mytischi/ms103/network_confrontation.git
```
2. Перейти в папку с проектом и инициализировать его
```bash
cd network_confrontation/project
./init.sh
```
При первом запуске скрипт попросит права администратора (чтобы установить `python3-venv`). После этого нужно будет указать пароль суперпользователя в web-части сайта (`promprog`)

3. Загрузить проект в PyCharm (открывать папку `network_confrontation/project`, тогда подгрузятся все части проекта)
4. Создать виртуальное окружение (через settings -> project "simple votings" -> project interpreter). Нужно использовать опцию "уже существующее виртуальное окружение" - в нём будут установлены все необходимые пакеты
5. Создать конфигурацию запуска в PyCharm (файл `src/web/manage.py`, опция `runserver`)
5. Создать конфигурацию запуска в PyCharm (файл `src/desktop/run.py`)
