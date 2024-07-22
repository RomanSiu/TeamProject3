* Створюєте файл .env по прикладу .env.example
* Створюєте докер БД $ docker run --name "назва контейнера" -p 5432:5432 -e POSTGRES_PASSWORD="пароль бази даних" -d postgres
* Створюєте докер редіса $ docker run --name redis-cache -d -p 6379:6379 redis
* Створюєте таблиці в БД $ alembic upgrade head
* Запускаєте API $ py main.py
