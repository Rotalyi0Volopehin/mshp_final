Настройка работы чата
=====================

Для фунционирования чата необходимо установить и запустить утилиту *Docker*.

Установка *Docker*
------------------

 #. Обновляем существующий перечень пакетов:
    ``sudo apt update``
 #. Устанавливаем необходимые пакеты, которые позволяют apt использовать пакеты по HTTPS:
    ``sudo apt install apt-transport-https ca-certificates curl software-properties-common``
 #. Добавляем в систему ключ GPG официального репозитория *Docker*:
    ``curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -``
 #. Добавляем репозиторий *Docker* в список источников пакетов APT:
    ``sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"``
 #. Обновим базу данных пакетов информацией о пакетах *Docker* из вновь добавленного репозитория:
    ``sudo apt update``
 #. Устанавливаем Docker:
    ``sudo apt install docker-ce``

Запуск *Docker*
---------------

 * Для того, чтобы запустить *Docker* на порту **6379** *(по умолчанию установлен в проекте)*, необходимо использовать следующий набор команд: ``sudo docker run -p 6379:6379 -d redis:5``

Изменение порта чата в проекте
------------------------------

Для того, чтобы сменить порт чата в проекте, нужно изменить строку ``CHANNEL_LAYERS_PORT = 6379`` в файле ``src/web/network_confrontation_web/settings.py``

Настройка локализации
---------------------

Если в проекте возникают ошибки, связанные с использованием кириллицы в сообщениях, надо экспортировать кодировку: ``export LC_ALL="ru_RU.UTF-8"``
