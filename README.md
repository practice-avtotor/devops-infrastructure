# DevOps Infrastructure for BOM System

Инфраструктура для системы автоматической сверки ведомостей материалов (BOM) с операционными картами сборки. Проект содержит Docker Compose конфигурацию для локального запуска всех сервисов.

## Содержание

- [Об архитектуре](#об-архитектуре)
- [Требования](#требования)
- [Быстрый старт](#быстрый-старт)
- [Доступ к сервисам](#доступ-к-сервисам)
- [Переменные окружения](#переменные-окружения)
- [Команды для разработки](#команды-для-разработки)
- [Структура проекта](#структура-проекта)
- [Устранение неполадок](#устранение-неполадок)

---

## Об архитектуре

Система состоит из четырёх основных компонентов, каждый из которых запускается в отдельном контейнере:

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| **Backend** | FastAPI + Uvicorn | REST API, бизнес-логика, обработка данных |
| **Frontend** | Vue 3 + Vite | Пользовательский интерфейс для загрузки файлов и просмотра отчётов |
| **Redis** | Redis 7 | Брокер сообщений для Celery (очередь задач) |
| **Celery Worker** | Celery | Асинхронная обработка (парсинг, сверка) — *в разработке* |

Все контейнеры объединены в общую сеть `bom-network` и обмениваются данными по именам сервисов (`backend`, `frontend`, `redis`).

---

## Требования

- **Docker** >= 24.0.0
- **Docker Compose** >= 2.20.0
- **Git** (для клонирования)

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/practice-avtotor/devops-infrastructure.git
cd devops-infrastructure
```

### 2. Настройка переменных окружения и локальных переопределений

Скопируйте примеры конфигурации:

```bash
cp .env.example .env
cp docker-compose.override.yml.example docker-compose.override.yml
```

При необходимости отредактируйте `.env` и `docker-compose.override.yml` под свои нужды.

### 3. Сборка и запуск всех сервисов

```bash
docker compose up --build
```

После успешного запуска вы увидите логи всех контейнеров.

### 4. Проверка работы

В зависимости от того, используете ли вы локальные переопределения (`docker-compose.override.yml`), доступ к сервисам осуществляется по-разному.

#### Вариант А: Локальная разработка (с `docker-compose.override.yml`)
* **Frontend:** http://localhost:5173
* **Backend API (Swagger):** http://localhost:8000/docs
* **Nginx Reverse Proxy:** http://localhost (проксирует запросы)

#### Вариант Б: Стандартный запуск (без `docker-compose.override.yml`)
* **Вся система (через Nginx):** http://localhost (порт 80)
* **Backend API (через Nginx):** http://localhost/api/v1/docs

---

## Доступ к сервисам

### При локальной разработке (с override)
| Сервис | Внутренний порт | Внешний порт | URL |
|--------|-----------------|--------------|-----|
| **Nginx (Proxy)** | 80 | 80 | http://localhost |
| **Frontend** | 5173 | 5173 | http://localhost:5173 |
| **Backend API** | 8000 | 8000 | http://localhost:8000/docs |
| **Redis** | 6379 | 6379 | `redis://localhost:6379` |

### При стандартном запуске (без override)
| Сервис | Внутренний порт | Внешний порт | URL |
|--------|-----------------|--------------|-----|
| **Nginx (Proxy)** | 80 | 80 | http://localhost |
| **Frontend** | 5173 | Не экспортируется | Доступен через Nginx (http://localhost) |
| **Backend API** | 8000 | Не экспортируется | Доступен через Nginx (http://localhost/api/v1/docs) |
| **Redis** | 6379 | Не экспортируется | Доступен только внутри сети `bom-network` |

---

## Переменные окружения

Файл `.env` содержит следующие переменные (шаблон в `.env.example`):

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `REDIS_URL` | Адрес для подключения к Redis | `redis://redis:6379/0` |
| `DB_URL` | Путь к файлу SQLite базы данных внутри контейнера | `/data/jobs.db` |
| `STORAGE_PATH` | Путь для хранения загруженных файлов внутри контейнера | `/data` |
| `BACKEND_PORT` | Внутренний порт бэкенда | `8000` |
| `FRONTEND_PORT` | Внутренний порт фронтенда | `5173` |

---

## Команды для разработки

### Запуск всех сервисов в фоновом режиме

```bash
docker compose up -d
```

### Остановка всех сервисов

```bash
docker compose down
```

### Пересборка конкретного сервиса

```bash
docker compose build --no-cache backend
docker compose up -d backend
```

### Просмотр логов

```bash
# Все логи
docker compose logs

# Логи конкретного сервиса
docker compose logs backend
docker compose logs frontend

# Логи в реальном времени
docker compose logs -f backend
```

### Проверка статуса контейнеров

```bash
docker compose ps
```

### Очистка данных (удаление томов)

```bash
docker compose down -v
```

---

## Структура проекта

```
devops-infrastructure/
├── docker-compose.yml          # Основная конфигурация сервисов
├── .env.example                # Пример переменных окружения
├── .gitignore
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD пайплайн (GitHub Actions) - *в разработке*
└── (внешние репозитории)
    ├── ../burlak-backend/      # Бэкенд (FastAPI)
    └── ../Burlak_frontend/     # Фронтенд (Vue 3)
```

> **Важно:** Репозитории с кодом (`burlak-backend` и `Burlak_frontend`) должны находиться на одном уровне с `devops-infrastructure`.

```
~/projects/
├── burlak-backend/
├── Burlak_frontend/
└── devops-infrastructure/      # ← Вы здесь
```

---

## Устранение неполадок

### Ошибка: `port is already allocated`

Порт 8000 или 5173 уже занят другим процессом.

```bash
# Найти процесс, использующий порт
sudo lsof -i :8000

# Остановить контейнеры
docker compose down
```

### Ошибка: `No such file or directory: ../burlak-backend`

Убедитесь, что репозитории расположены правильно:

```bash
ls -la ~/projects/
# Должны быть: burlak-backend/, Burlak_frontend/, devops-infrastructure/
```

### Ошибка сборки фронтенда

Попробуйте использовать `build-only` вместо `build` в Dockerfile:

```dockerfile
RUN npm run build-only
```

---

## Лицензия

Проект разработан в рамках производственной практики в АО «Автотор».
