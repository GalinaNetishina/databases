# Парсер результатов торгов в БД

Установить зависимости
```bash
pip install -r requirements.txt
```

Заполнить .env и загрузить данные
```bash
python main.py
```

Для проверки запустить сервер
```bash
cd ./databases/task2
uvicorn main:app 
```
[просмотр](http://127.0.0.1:8000/docs#/)


# Создание БД для доставки книг

Для проверки запустить сервер
```bash
cd ./databases/task1
uvicorn app:app 
```
[просмотр](http://127.0.0.1:8000/docs#/)

[другой вариант, когда данные внесены](http://127.0.0.1:8000/index/authors)