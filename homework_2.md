## Задание 1:
1) запустить контейнер с ubuntu, используя механизм LXC
2) ограничить контейнер 256 Мб ОЗУ и проверить, что ограничение работает
3) добавить автозапуск контейнеру, перезагрузить ОС и убедиться, что контейнер действительно запустился самостоятельно
4) при создании указать файл, куда записывать логи
5) после перезагрузки проанализировать логи

Установка пакетов lxc:

**apt install lxc**

**apt install lxc-templates**

**apt install lxd-installer**

**lxd init** - запуск службы lxd

* Настройка

**lxc-create -n homework -t ubuntu** - создали контейнер
**lxc-ls -f** - проверяем состояние установленных пакетов

* Запускаем конфигурационный файл:

**vim /var/lib/lxc/homework/config**

* Вводим настройки ограничения памяти и автоматического запуска контейнера

* * *
* Содержимое файла

**lxc.include = /usr/share/lxc/config/ubuntu.common.conf

lxc.init.cmd = /sbin/init systemd.unified_cgroup_hierarchy=1**

* * *
* Container specific configuration

**lxc.rootfs.path = dir:/var/lib/lxc/homewrok/rootfs**

**lxc.uts.name = homework**

**lxc.arch = amd64**

* * *
* Network configuration
  
**lxc.net.0.type = veth**

**lxc.net.0.link = lxcbr0**

**lxc.net.0.flags = up**

* Задаем ip (для задания 2)

**lxc.net.0.ipv4.address = 10.0.13.0/24**

**lxc.net.0.hwaddr = 00:16:3e:0c:ed:82**

**lxc.cgroup2.memory.max = 256M** #ограничение памяти

**lxc.start.auto  =  1** #автоматический старт
* * *
Запускаем контейнер
lxc-start -d -n homework - Скриншот 2

* Заходим в контейнер:
* 
**lxc-attach -n homework**

*Проверяем память:

**free -m**

* Выходим из контейнера и останавливаем его:

**exit**

**lxc-stop -n homework**

* Проверяем состояние контейнера:

**lxc-ls -f**

* Перезагружаем ОС

* Проверяем статус контейнера после перезагрузки:
  
**lxc-ls -f**

* Останавливаем контейнер:

**lxc-stop -n homework**

* Запускаем контейнер с записью логов в файл **homework_start.log**

**lxc-start -n test123 --logfile /var/log/homework_start.log**

* После выхода из контейнера файл с логами пуст, т.к. не было ошибок в работе контейнера - Скриншот 7

## Задание 2:
настроить автоматическую маршрутизацию между контейнерами.

Адреса можно взять: 10.0.12.0/24 и 10.0.13.0/24.

* Аналогично создаем контейнер tobridge и задаем его настройки:

**lxc-create -n tobridge -t ubuntu** - создали контейнер

* Запускаем конфигурационный файл:

**vim /var/lib/lxc/tobridge/config**

* Вводим настройки ограничения памяти и автоматического запуска контейнера

* * *
* Содержимое файла
**lxc.include = /usr/share/lxc/config/ubuntu.common.conf**

**lxc.init.cmd = /sbin/init systemd.unified_cgroup_hierarchy=1**

* Container specific configuration

**lxc.rootfs.path = dir:/var/lib/lxc/tobridge/rootfs**

**lxc.uts.name = tobridge**

**lxc.arch = amd64**

* Network configuration

**lxc.net.0.type = veth**

**lxc.net.0.link = lxcbr0**

**lxc.net.0.flags = up**

**lxc.net.0.ipv4.address = 10.0.13.0/24**

**lxc.net.0.hwaddr = 00:16:3e:0c:ed:82**
* * *

* Запускаем контейнер

**lxc-start -d -n homework**

* Проверка состояния контейнеров

**lxc-ls -f**

* Заходим в контейнер:

**lxc-attach -n tobridge**

* Запускаем команду:

**ping 10.0.13.0**
