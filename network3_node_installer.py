import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import paramiko
import time

# Загрузка настроек из .env файла
load_dotenv()

# Настройки из .env
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
GOOGLE_WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME")
START_ROW_PROMPT = "Введите номер начальной строки: "

# Подключение к Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_CREDENTIALS_FILE"), scope)
client = gspread.authorize(credentials)

# Заменяем названия таблицы и листа из настроек
spreadsheet = client.open(GOOGLE_SHEET_NAME)
sheet = spreadsheet.worksheet(GOOGLE_WORKSHEET_NAME)

# Считывание данных из таблицы
start_row = int(input(START_ROW_PROMPT))
data = sheet.get_all_values()[start_row - 1:]

# Подключение к серверам и выполнение скрипта
def run_script_on_server(ip, password, row_index):
    try:
        print(f"Подключение к серверу {ip}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="root", password=password)

        print("Скачивание скрипта...")
        stdin, stdout, stderr = ssh.exec_command("wget -O network3_node_installer.sh https://raw.githubusercontent.com/fl77ex/network3_node_installer/refs/heads/main/network3_node_installer.sh && chmod +x network3_node_installer.sh")
        print(stdout.read().decode(), stderr.read().decode())

        print("Запуск скрипта установки...")
        stdin, stdout, stderr = ssh.exec_command("bash network3_node_installer.sh")
        print(stdout.read().decode(), stderr.read().decode())

        print("Получение API ключа...")
        stdin, stdout, stderr = ssh.exec_command("cd")
        time.sleep(5)
        stdin, stdout, stderr = ssh.exec_command("cd ubuntu-node && sudo bash manager.sh key")
        output = stdout.read().decode().strip()

        # Извлечение последней строки как API ключа
        api_key = output.splitlines()[-1] if output else None

        if not api_key or len(api_key) < 10:  # Проверка на валидность ключа
            print(f"Не удалось извлечь API ключ для сервера {ip}. Полный вывод: \n{output}")
            return

        print(f"API Key получен: {api_key}")

        # Сохраняем API KEY в столбец F
        print(f"Сохранение API Key в таблице для сервера {ip}...")
        sheet.update_cell(row_index, 6, api_key)  # Столбец F имеет индекс 6

        print(f"API Key для сервера {ip} успешно сохранен.")

        ssh.close()

    except Exception as e:
        print(f"Ошибка при подключении к серверу {ip}: {e}")

# Основной цикл для обработки данных из таблицы
for i, row in enumerate(data, start=start_row):
    ip, password = row[2], row[3]
    print(f"Обработка сервера {ip}...")
    run_script_on_server(ip, password, i)
    print(f"Сервер {ip} обработан.\n\n")
    time.sleep(2)

print("Все сервера обработаны. Завершено.")
