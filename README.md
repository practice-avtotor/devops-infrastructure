# DevOps Infrastructure for BOM System

Инфраструктура для системы автоматической сверки ведомостей материалов (BOM) с операционными картами сборки. Проект содержит Docker Compose конфигурацию для локального запуска всех сервисов.

## Содержание

- [Об архитектуре](#-об-архитектуре)
- [Требования](#-требования)
- [Быстрый старт](#-быстрый-старт)
- [Доступ к сервисам](#-доступ-к-сервисам)
- [Переменные окружения](#-переменные-окружения)
- [Команды для разработки](#-команды-для-разработки)
- [Структура проекта](#-структура-проекта)
- [Устранение неполадок](#-устранение-неполадок)

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

### 2. Настройка переменных окружения

Скопируйте пример конфигурации:

```bash
cp .env.example .env
```

При необходимости отредактируйте `.env` под свои нужды.

### 3. Сборка и запуск всех сервисов

```bash
docker compose up --build
```

После успешного запуска вы увидите логи всех контейнеров.

### 4. Проверка работы

Откройте в браузере:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/docs (Swagger)
- **Backend:** http://localhost:8000/

---

## 🔌 Доступ к сервисам

| Сервис | Порт | URL | Логин/Пароль |
|--------|------|-----|--------------|
| **Frontend** | 5173 | http://localhost:5173 | — |
| **Backend API** | 8000 | http://localhost:8000/docs | — |
| **Redis** | 6379 | `redis://localhost:6379` | — |

---

## Переменные окружения

Файл `.env` содержит следующие переменные:

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `REDIS_URL` | Адрес для подключения к Redis | `redis://redis:6379/0` |
| `SQLITE_DB_PATH` | Путь к файлу SQLite базы данных | `/app/data/tasks.db` |
| `STORAGE_PATH` | Путь для хранения загруженных файлов | `/app/storage` |

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

## Лицензия

Проект разработан в рамках производственной практики в АО «Автотор».
