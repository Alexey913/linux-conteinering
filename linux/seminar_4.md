1. Подключить дополнительный репозиторий на выбор: Docker, Nginx, Oracle MySQL. Установить любой пакет из этого репозитория.
- Переходим в режим root – команда sudo su, вводим пароль
- Обновляем информацию о репозиториях, указанных в настройках – команда apt update
- Устанавливаем дополнительные пакеты, необходимые для установки – команды

    **apt-get install \**
  
    **ca-certificates \**
  
    **curl \**
  
    **gnupg \**
  
    **lsb-release**
  
- Добавляем ключ gpg – команды

**mkdir -m 0755 -p /etc/apt/keyrings**

**curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg**

- Добавляем репозиторий – команда

**echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null**
- Обновляем информацию о репозиториях, указанных в настройках – команда **apt update**
- Устанавливаем Docker – команда

**apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin**

2. Установить и удалить deb-пакет с помощью dpkg
- Делаем на примере Virtualbox.
- Скачиваем пакет – команда **wget https://download.virtualbox.org/virtualbox/7.0.6/virtualbox-7.0_7.0.6-155176~Ubuntu~jammy_amd64.deb**
- Распаковываем пакет **dpkg -i virtualbox-7.0_7.0.6-155176~Ubuntu~jammy_amd64.deb**
- Устанавливаем недостающие пакеты – команда **apt -f install**

3. Установить и удалить snap-пакет.

Ищем пакеты – команда **snap search**
Устанавливаем пакет spotify – команда **snap install spotify**

5. Добавить задачу для выполнения каждые 3 минуты (создание директории, запись в файл)

Переходим в папку etc – команда **cd /etc**

Открываем файл crontab – команда **vim crontab**

Прописываем команду для создания директории - */3 *   * * *   **root mkdir /root/director**
