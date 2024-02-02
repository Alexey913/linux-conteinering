## Задание

* нужно создать 2 ДК-файла, в которых будут описываться сервисы
* повторить задание 1 для двух окружений: lab, dev
* обязательно проверить и зафиксировать результаты, чтобы можно было выслать преподавателю для проверки

### [Содержимое скрипта 1]()
### {Содержимое скрипта 2}()

* В первой ноде запускаем Docker Swarm

**docker swarm init**

* Получаем токен:
  
**docker swarm join --token SWMTKN-1-3zazcnzotdq7uv8nc9vzf9uf0or2518dltrysa59a29gqkbkri-67raoadax0l92p4jdmiyk3k2j 192.168.0.106:2377**

* Проверяем список нод:

**docker node ls**

* В новой машине подключаемся к серверу, введя токен

**docker swarm join --token SWMTKN-1-5e3w7d98nxexiew0epb0ehb009ay6qolv5uc4amtgtavyd1axb-8263dctt5fc923wphqei98sc4 192.168.0.106:2377**

* Повторно проверяем список нод:

**docker node ls**

* Создаем виртуальную сеть:

**docker network ls** - проверяем существующие сети

**docker network create --driver overlay --subnet 4.5.6.0/24 homework-net --attachable** - создание новой сети

**docker network ls** - проверяем, что сеть создана

* В главной ноде создаем сервер maria-db:

**docker service create --name mariadb_service --replicas 2 -e MYSQL_ROOT_PASSWORD=12345 --network homework-net -p 3036:3036 mariadb:10.10.2**

* В главной ноде создаем сервер php-myadmin, экземпляры которого запустятся на каждой ноде:

**docker service create --name my-phpmyadmin --mode=global -e PMA_HOST=mariadb_service --network homework-net -p 8081:80 phpmyadmin/phpmyadmin**

* Проверяем созданные сервисы:

**docker service ps mariadb_service**

**docker service ps my-phpmyadmin**

* Запуск через браузер

* Присваиваем вторую ноду к продуктивному контуру:

**docker node update --label-add env=prod nealex-VirtualBox**

* Проверяем информацию о ноде:

**docker node inspect nealex-VirtualBox**

* Создаем сервис, который будет запускаться только в продуктивном контуре:

**docker service create --name mariadb_service_prod --constraint node.labels.env==prod --replicas 3 -e MYSQL_ROOT_PASSWORD=12345 -p 3306:3306 mariadb:10.10.2**

* Проверяем созданный сервис в обеих нодах:

**docker service ps mariadb_service_prod**

* Запуск docker compose:
**docker compose up -d** #неудача

* Проверяем созданные сервисы
**docker compose ps**

* Запуск сервиса через docker-compose:
**docker stack deploy -с docker-compose.yaml STACK** #неудача
