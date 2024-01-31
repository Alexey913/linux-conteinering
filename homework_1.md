## 1. Изоляция процесса в NameSpace PID
echo $$

sudo unshare -p --fork bash

echo $$

cd /proc/$$/ns

## 2. Изоляция процесса в NameSpace NET
**sudo unshare -n bash (терминал 2)**

* в терминале 2 проверяем наличие процесса

**sudo lsns | grep bash**

## 3. Изоляция процесса в NameSpace UTS
**sudo unshare -u bash**

* меняем hostname

**hostname test**

* в терминале 2 проверяем hostname

**hostname**

## 4. Изоляция процесса в NameSpace USER
**sudo unshare -U bash**

## В пп. 1-4 процессы являются вложенными. Если необходимо сделать один процесс с нужными параметрами:
**sudo unshare -p -u -U --net --fork bash**
