network3_node_installer.sh work standalone at server

network3_node_installer.py get ip and pass of the server from Google Sheet (C,D columns) and put node's API KEY at F column

Work time approx 3 min for 1 node

.env example

# Название Google таблицы
GOOGLE_SHEET_NAME=Table name

# Название листа в таблице
GOOGLE_WORKSHEET_NAME=Sheet name

# Путь к JSON файлу с ключами для авторизации в Google API
GOOGLE_CREDENTIALS_FILE=credentials.json
