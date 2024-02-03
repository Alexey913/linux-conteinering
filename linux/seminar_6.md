## Задание:

1. Установить Nginx и настроить его на работу с PHP-FPM.
2 Установить Apache. Настроить обработку PHP. Добиться одновременной работы с Nginx.
3. Настроить схему обратного прокси для Nginx (динамика - на Apache).
4. Установить MySQL. Создать новую базу данных и таблицу в ней.
5* Установить пакет phpmyadmin и запустить его веб-интерфейс для управления MySQL.
6* Настроить схему балансировки трафика между несколькими серверами Apache на стороне Nginx с помощью модуля ngx_http_upstream_module.

## Результат:
1. Установить Nginx и настроить его на работу с PHP-FPM.

Установка – команда **sudo apt install nginx**

Настройка конфигурации ngnix:

	location ~ \.php$ {
		       include snippets/fastcgi-php.conf;
		       root /var/www/html;
		       fastcgi_pase unix:/run/php/php8.1-fpm.sock;
	}

2 Установить Apache. Настроить обработку PHP. Добиться одновременной работы с Nginx.

Установка – команда **sudo apt install apache2 apachectl -t**

Тестируем конфигурацию – команда **apachectl -t**

Применяем текущую конфигурацию – команда **sudo systemctl reload apache2
**
Добавляем обработку PHP – команда **apt install libapache2-mod-php8.1 php8.1**

Обработка PHP подключается автоматически

Создаём файл для проверки с текстом:

	<?php
	phpinfo();
	?>
 
Проверка – команда **curl http://localhost/info.php**

3. Настроить схему обратного прокси для Nginx (динамика - на Apache).

Вводим следующую конфигурацию:

Для динамических запросов

	location / {
	       proxy_pass http://localhost:8080;
	       proxy_set_header Host $host;
	       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	       proxy_set_header X-Real-IP $remote_addr;
	}

Для статических запросов

	location ~* ^.+.(jpg|jpeg|gif|png|ico|css|zip|pdf|txt|tar|js)$ {
	       root /var/www/html;
	}

4. Установить MySQL. Создать новую базу данных и таблицу в ней.

Установка – команда **apt install mysql-server-8.0**

Заходим в консоль mysql – команда **sudo mysql**

Переходим в системную БД mysql – команда **use mysql;**

Получаем список пользователей – команда **SELECT * FROM user\G**

Создаём новую БД – команда **CREATE DATABASE gb;**

Создаём таблицу – команда **CREATE TABLE new_table(i INT);**

Создадим записи в таблице – команда **INSERT INTO test (i) VALUES (1),(2),(3),(4);**

Выборка из таблицы – команда **SELECT * FROM new_table;**

Выход из mysql – команда **exit**

5* Установить пакет phpmyadmin и запустить его веб-интерфейс для управления MySQL.

Команда **sudo apt install phpmyadmin**

6* Настроить схему балансировки трафика между несколькими серверами Apache на стороне Nginx с помощью модуля ngx_http_upstream_module.

Вводим следующую конфигурацию:
	upstream backend {
		server 127.0.0.1:8080 weight=2;
		server 127.0.0.1:8081;
	}
	
	server {
		listen 80 default_server;
		listen [::]:80 default_server;
	
	root /var/www/html;
	server_name_;
	
		location / {
			proxy_pass http://backend;
	proxy_set_header Host $host;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Real-IP $remote_addr;
}
