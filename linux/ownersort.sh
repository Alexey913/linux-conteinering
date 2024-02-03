#!/bin/bash

#Создать скрипт ownersort.sh, который в заданной папке копирует файлы в директории,
#названные по имени владельца каждого файла.
#Учтите, что файл должен принадлежать соответствующему владельцу.

if [ -d $1 ]
	then
		echo "Directory found!"
	else
		echo "Error directory!"
		exit 2
fi

directory=$1
for i in $(ls ${directory})
do
	file_owner="stat -c '%U' $i"
	mv $i /alex/to_users/${file_owner}
done
echo "Files are removed!"