## Задание:
Установить в виртуальную машину или VDS Docker, настроить набор контейнеров через docker compose по инструкции по ссылке: https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-with-docker-compose-ru. Часть с настройкой certbot и HTTPS опустить, если у вас нет настоящего домена и белого IP.

## Результат:
1. Установка Docker – **sudo apt install docker.io**

2. Установка Docker-compose - **sudo apt install docker-compose**

3. Переходим в режим root – **sudo su**

4. Настройка конфигурации веб-сервера:

**mkdir wordpress && cd wordpress**

**mkdir nginx-conf**

**vim nginx-conf/nginx.conf**

6. Вводим содержимое файла конфигурации:

        server {
                listen 80;
                listen [::]:80;
        
                server_name skoroleto2023.com www.skoroleto2023.com;
        
                index index.php index.html index.htm;
        
                root /var/www/html;
        
                location ~ /.well-known/acme-challenge {
                        allow all;
                        root /var/www/html;
                }
        
                location / {
                        try_files $uri $uri/ /index.php$is_args$args;
                }
        
                location ~ \.php$ {
                        try_files $uri =404;
                        fastcgi_split_path_info ^(.+\.php)(/.+)$;
                        fastcgi_pass wordpress:9000;
                        fastcgi_index index.php;
                        include fastcgi_params;
                        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                        fastcgi_param PATH_INFO $fastcgi_path_info;
                }
        
                location ~ /\.ht {
                        deny all;
                }
        
                location = /favicon.ico {
                        log_not_found off; access_log off;
                }
                location = /robots.txt {
                        log_not_found off; access_log off; allow all;
                }
                location ~* \.(css|gif|ico|jpeg|jpg|js|png)$ {
                        expires max;
                        log_not_found off;
                }
        }

7. Настройка переменных среды:

**vim .env**

Содержимое файла:

        MYSQL_ROOT_PASSWORD=2409
        MYSQL_USER=alex
        MYSQL_PASSWORD=2409
        vim .dockerignore
        Содержимое файла:
        .env
        .git
        docker-compose.yml
        .dockerignore

8. Определение служб с помощью Docker Compose:

**vim docker-compose.yml**

Содержимое файла:

        version: '3'
        
        services:
          db:
            image: mysql:8.0
            container_name: db
            restart: unless-stopped
            env_file: .env
            environment:
              - MYSQL_DATABASE=wordpress
            volumes:
              - dbdata:/var/lib/mysql
            command: '--default-authentication-plugin=mysql_native_password'
            networks:
              - app-network
        
          wordpress:
            depends_on:
              - db
            image: wordpress:5.1.1-fpm-alpine
            container_name: wordpress
            restart: unless-stopped
            env_file: .env
            environment:
              - WORDPRESS_DB_HOST=db:3306
              - WORDPRESS_DB_USER=$MYSQL_USER
              - WORDPRESS_DB_PASSWORD=$MYSQL_PASSWORD
              - WORDPRESS_DB_NAME=wordpress
            volumes:
              - wordpress:/var/www/html
            networks:
              - app-network
        
          webserver:
            depends_on:
              - wordpress
            image: nginx:1.15.12-alpine
            container_name: webserver
            restart: unless-stopped
            ports:
              - "80:80"
            volumes:
              - wordpress:/var/www/html
              - ./nginx-conf:/etc/nginx/conf.d
              - certbot-etc:/etc/letsencrypt
            networks:
              - app-network
        
          certbot:
            depends_on:
              - webserver
            image: certbot/certbot
            container_name: certbot
            volumes:
              - certbot-etc:/etc/letsencrypt
              - wordpress:/var/www/html
            command: certonly --webroot --webroot-path=/var/www/html --email al913@mail.ru --agree-tos --no-eff-email al913@mail.ru --staging -d skoroleto2023.com -d www.skoroleto2023.com
        
        volumes:
          certbot-etc:
          wordpress:
          dbdata:
        
        networks:
          app-network:
            driver: bridge  

9. Получение сертификатов SSL и учетных данных:

**docker-compose up -d**

**docker-compose ps**

**docker-compose exec webserver ls -la /etc/letsencrypt/live**

**vim docker-compose.yml**

Меняием флаг **--staging** в параметрах command на флаг **--force-renewal**:

          certbot:
            depends_on:
              - webserver
            image: certbot/certbot
            container_name: certbot
            volumes:
              - certbot-etc:/etc/letsencrypt
              - certbot-var:/var/lib/letsencrypt
              - wordpress:/var/www/html
            command: certonly --webroot --webroot-path=/var/www/html --email sammy@example.com --agree-tos --no-eff-email al913@mail.ru --force-renewal -d skoroleto2023.com -d www.skoroleto2023.com
        
        docker-compose up --force-recreate --no-deps certbot – запрос сертификата выполнен

10. Изменение конфигурации веб-сервера и определения службы

**docker-compose stop webserver**

**curl -sSLo nginx-conf/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf**

**rm nginx-conf/nginx.conf**

**vim nginx-conf/nginx.conf**

Меняем содержимое файла:

        server {
                listen 80;
                listen [::]:80;
        
                server_name example.com www.example.com;
        
                location ~ /.well-known/acme-challenge {
                        allow all;
                        root /var/www/html;
                }
        
                location / {
                        rewrite ^ https://$host$request_uri? permanent;
                }
        }
        
        server {
                listen 443 ssl http2;
                listen [::]:443 ssl http2;
                server_name skoroleto2023.com www.skoroleto2023.com;
        
                index index.php index.html index.htm;
        
                root /var/www/html;
        
                server_tokens off;
        
                ssl_certificate /etc/letsencrypt/live/skoroleto2023.com/fullchain.pem;
                ssl_certificate_key /etc/letsencrypt/live/skoroleto2023.com/privkey.pem;
        
                include /etc/nginx/conf.d/options-ssl-nginx.conf;
        
                add_header X-Frame-Options "SAMEORIGIN" always;
                add_header X-XSS-Protection "1; mode=block" always;
                add_header X-Content-Type-Options "nosniff" always;
                add_header Referrer-Policy "no-referrer-when-downgrade" always;
                add_header Content-Security-Policy "default-src * data: 'unsafe-eval' 'unsafe-inline'" always;
                # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
                # enable strict transport security only if you understand the implications
        
                location / {
                        try_files $uri $uri/ /index.php$is_args$args;
                }
        
                location ~ \.php$ {
                        try_files $uri =404;
                        fastcgi_split_path_info ^(.+\.php)(/.+)$;
                        fastcgi_pass wordpress:9000;
                        fastcgi_index index.php;
                        include fastcgi_params;
                        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                        fastcgi_param PATH_INFO $fastcgi_path_info;
                }
        
                location ~ /\.ht {
                        deny all;
                }
        
                location = /favicon.ico {
                        log_not_found off; access_log off;
                }
                location = /robots.txt {
                        log_not_found off; access_log off; allow all;
                }
                location ~* \.(css|gif|ico|jpeg|jpg|js|png)$ {
                        expires max;
                        log_not_found off;
                }
        }

**vim docker-compose.yml**

Меняем содержимое файла:
        webserver:
            depends_on:
              - wordpress
            image: nginx:1.15.12-alpine
            container_name: webserver
            restart: unless-stopped
            ports:
              - "80:80"
              - "443:443"
            volumes:
              - wordpress:/var/www/html
              - ./nginx-conf:/etc/nginx/conf.d
              - certbot-etc:/etc/letsencrypt
            networks:
              - app-network

Повторно создаем службу **webserver - docker-compose up -d --force-recreate --no-deps webserver**

**docker-compose ps**

11. Завершение установки через веб-интерфейс

Выбор языка

Обновление сертификатов:
**vim ssl_renew.sh**

Содержимое файла:

        #!/bin/bash
        
        COMPOSE="/usr/local/bin/docker-compose --no-ansi"
        DOCKER="/usr/bin/docker"
        
        cd /home/sammy/wordpress/
        $COMPOSE run certbot renew --dry-run && $COMPOSE kill -s SIGHUP webserver
        $DOCKER system prune -af
        
        chmod +x ssl_renew.sh
        crontab -e

Добавляем строку:

***/5 * * * * /home/sammy/wordpress/ssl_renew.sh >> /var/log/cron.log 2>&1**

Проверка: **tail -f /var/log/cron.log**
