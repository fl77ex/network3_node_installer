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

# Настраиваем автозапуск ноды после перезагрузки
cat <<EOL | sudo tee /etc/systemd/system/network3-node.service
[Unit]
Description=Network 3 Node Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'cd /root/ubuntu-node && sudo bash manager.sh up'
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOL

# Перезапускаем демоны systemd и включаем службу
sudo systemctl daemon-reload
sudo systemctl enable network3-node.service
sudo systemctl start network3-node.service

# Функция для получения API Key
function get_api_key {
  while true; do
    output=$(sudo bash manager.sh key)
    echo "$output"

    # Извлекаем последнюю строку
    last_line=$(echo "$output" | tail -n 1)

    if [[ "$last_line" != "System architecture is x86_64 (64-bit)" ]]; then
      echo "API Key успешно получен!"
      break
    else
      echo "Не удалось получить API Key. Повтор через 5 секунд..."
      sleep 5
    fi
  done
}

# Запрашиваем API Key
get_api_key

