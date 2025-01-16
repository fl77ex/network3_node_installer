#!/bin/bash

# Устанавливаем безопасный umask
umask 077

# Обновляем все файлы
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые приложения
sudo apt install -y screen net-tools iptables

# Устанавливаем Network 3 Node
wget https://network3.io/ubuntu-node-v2.1.1.tar.gz

# Разархивируем файл и переходим в папку убунты
tar -xvf ubuntu-node-v2.1.1.tar.gz
rm -rf ubuntu-node-v2.1.1.tar.gz
cd ubuntu-node

# Создаем Screen сессию ноды
screen -S network3 
sudo bash manager.sh up

# Выводим API KEY в консоль
sudo bash manager.sh key
