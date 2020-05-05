#### Script

Для запуска сервера:

в script.py Изменить 
#### PASS 
на корневой каталог сервера.

Проверить порт в port.txt, проверить путь к 
#### default-bot

Запуск: python3 script.py.


#### Запросы:

все методы POST

#### 1:

http://127.0.0.1:5000/create

Копирует папку default-bot в папку <port>-bot (port изначально задан в файле port.txt)

выполняет docker-compose build

Ответ: answer = {'status': 'created', 'port': port}

#### 2:

http://127.0.0.1:5000/start/<port>

выполняет команду docker-compose up -d в папке бота по присланному порту

Ответ: {"Port": "5051", "Status": "Started"}

#### 3:

http://127.0.0.1:5000/down/<port>

выполняет команду docker-compose down в папке бота по присланному порту

Ответ: { "Port": "5051", "Status": "Downed"}

#### 4:

 http://127.0.0.1:5000/delete
 
 выполняет docker container prune -f (удаление остановленных контейнеров)
 
 Ответ: {"Status": "Deleted"}
 
 #### 5:
 
 http://127.0.0.1:5000/deleteall
 
 на всякий случай для остановки и удаления всех докеров : docker rm -f $(docker ps -a -q)
 
 Ответ: {"Status": "Deleted all"}
 
 
 


 
 
 
