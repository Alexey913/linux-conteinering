#!/bin/bash

#Написать скрипт очистки директорий.
#На вход принимает путь к директории.
#Если директория существует, то удаляет в ней все файлы с расширениями .bak, .tmp, .backup.
#Если директории нет, то выводит ошибку.

if [ -d $1 ]
	then
		echo "Directory found!"
	else
		echo "Error directory!"
		exit 2
fi

directory=$1
find ${directory} \( -name "*.bak" -o -name "*.tmp" -o -name "*.backup" \) -delete
echo "Files is deleted!"