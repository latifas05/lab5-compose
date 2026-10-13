# Лабораторная работа №5: Multi-container приложение с Docker Compose

##  Структура проекта
- `api/` — исходный код Backend API (Flask), Dockerfile и зависимости.
- `docker-compose.yml` — конфигурация мультиконтейнерного приложения.
- `.env.example` — шаблон переменных окружения.

---

##  Инструкция по запуску

1. Создайте `.env` файл на основе `.env.example`.
2. Соберите и запустите контейнеры:
   ```bash
   docker compose up --build -d

##  Результаты тестирования
1. Статус контейнеров (docker compose ps)
<img width="913" height="65" alt="image" src="https://github.com/user-attachments/assets/88f1982e-e91f-4d86-bcee-ffa02b2abdfc" />

2. Health check
<img width="434" height="25" alt="image" src="https://github.com/user-attachments/assets/e4678451-04a3-4f92-a794-69ec7f9d419b" />

3. Проверка базы данных (/db-test)
<img width="697" height="26" alt="image" src="https://github.com/user-attachments/assets/eab485ba-e9db-40cc-b945-de3d3cfdd68f" />

4. Проверка кэша Redis (/cache-test)
<img width="680" height="29" alt="image" src="https://github.com/user-attachments/assets/f6670aa3-2abb-4cde-93f2-ca57972cdd80" />

5. Создать пользователя (/users)
<img width="956" height="86" alt="image" src="https://github.com/user-attachments/assets/89de9868-b4b4-4791-9df0-f8c9dc0eb35b" />

6. Получить пользователей
<img width="653" height="400" alt="image" src="https://github.com/user-attachments/assets/3fb6e61e-33fc-4791-9455-f2b54162f9f2" />

7. Зайти в контейнер API
<img width="125" height="26" alt="image" src="https://github.com/user-attachments/assets/a8dc0a94-eec1-4bc0-b6bf-2c508bf4bc9c" />

