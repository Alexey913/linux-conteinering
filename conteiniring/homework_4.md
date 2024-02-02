## Задание
необходимо создать Dockerfile, основанный на любом образе (вы в праве выбрать самостоятельно). В него необходимо поместить приложение, написанное на любом известном вам языке программирования (Python, Java, C, С#, C++). При запуске контейнера должно запускаться самостоятельно написанное приложение.

* Создаем скрипт Python:

**vim python_app.py**

[Содержимое скрипта](conteiniring/python_app_hw_4)

* Создаем файл для образа:

**vim homework4**

* Вводим в файле homework4 следующие строки:

**FROM python:3.10** #за основу берем образ python 3.10

**ADD python_app.py .** #добавляем в образ ранее созданный скрипт python

**CMD ["python3", "-i", "./python_app.py"]** #используем интерактивный режим, т.к. понадобится ввод данных пользователя

[Содержимое файла homework4](conteiniring/homework4)

* Создаем образ

**docker build -f homework4 -t homework4**

* Проверяем созданные образы

**docker images -a .**

* Запускаем образ

**docker run --rm -i homework4**

При запуске образа используем автоматичкое удаление, а также вход в интерактивном режиме для возможности ввода данных пользователя