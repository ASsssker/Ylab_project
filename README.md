# Ylab_project
## Запуск проекта

 1. Клонировать репозиторий
 `git clone https://github.com/ASsssker/Ylab_project.git`

 2. Перейти в папку с проектом
 3. Запустить проект командой
 `docker compose up --build -d`
 4. Для остановки проекта использовать команду
 `docker compose down`
 5. API будет доступно по ссылке
 `http://127.0.0.1:8000/api/v1`

 ## Запуск тестов
 1. Клонировать репозиторий
 `git clone https://github.com/ASsssker/Ylab_project.git`
 2. Перейти в папку с проектом
 3. Запустить тесты командой
 `docker compose -f docker-compose-test.yml up --build -d && docker logs --follow app && docker compose down -v
`
4. Результаты прохождения тестов будут выведены в терминал
5. Реализация функции `reverse` лежит в `tests/utils`
