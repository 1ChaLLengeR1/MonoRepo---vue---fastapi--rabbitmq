# MonoRepo - System Zarządzania Użytkowników z Frontend Vue.js

Projekt demonstracyjny systemu mikrousług z synchronizacją baz danych przy użyciu RabbitMQ, Celery i interfejsem użytkownika Vue.js.

## 📋 Opis Projektu

Kompletny system składający się z:
- **frontend** - aplikacja Vue.js z TypeScript do zarządzania użytkownikami
- **main_backend** - zarządza bazą `UserOne` przez REST API
- **service_backend** - zarządza bazą `UserTwo` przez komunikaty RabbitMQ

Główny cel: **pełna aplikacja webowa z automatyczną synchronizacją baz danych poprzez RabbitMQ przy każdej operacji CRUD**.

## 🏗️ Architektura Systemu

```

   Frontend              main_backend          RabbitMQ          service_backend
   (Vue.js)       ←→     (REST API)       →   (Messaging)      →   (Consumer)
      ↓                                                                ↓
   Browser               PostgreSQL             Redis              PostgreSQL
   :5173                 (UserOne)             (Celery)            (UserTwo)

```

## 🚀 Jak Uruchomić Projekt

### Wymagania
- Docker
- Docker Compose

### Uruchomienie
```bash
# Klonowanie repozytorium
git clone <repo-url>
cd MonoRepo

# Uruchomienie wszystkich serwisów
docker-compose up -d

# Sprawdzenie statusu kontenerów
docker-compose ps
```

### Dostęp do aplikacji
- **Frontend**: http://localhost:5173
- **Main Backend API**: http://localhost:3000
- **Service Backend API**: http://localhost:4000
- **RabbitMQ Panel**: http://localhost:15672 (guest/guest)

## 🐳 Serwisy Docker

| Serwis | Port | Opis |
|--------|------|------|
| **frontend** | 5173 | Vue.js - aplikacja webowa |
| **backend_main** | 3000 | FastAPI - główny backend z REST API |
| **backend_service** | 4000 | FastAPI - serwis z consumerem RabbitMQ |
| **celery_worker** | - | Worker Celery do przetwarzania zadań |
| **postgres_main** | 5450 | Baza danych dla UserOne |
| **postgres_service** | 5434 | Baza danych dla UserTwo |
| **rabbitmq** | 5672, 15672 | Message broker (panel: http://localhost:15672) |
| **redis** | 6379 | Backend dla Celery |

## 🎨 Frontend (Vue.js)

### Technologie
- **Vue 3** z Composition API
- **TypeScript**
- **Vite** jako build tool
- **SASS/SCSS** do stylowania
- **Vue Router** do routingu

### Komponenty
- `ShowFormCreateUser.vue` - przycisk do pokazania formularza
- `FormCreateUser.vue` - formularz tworzenia użytkownika
- `ListUser.vue` - lista użytkowników z opcjami edycji/usuwania
- `ListTask.vue` - lista zadań Celery

### API Client
Kompletny system komunikacji z backend'em:
- **GET** - pobieranie danych
- **POST** - tworzenie użytkowników
- **PATCH** - aktualizacja użytkowników
- **DELETE** - usuwanie użytkowników

### Uruchomienie w trybie deweloperskim
```bash
cd frontend
pnpm install
pnpm dev
```

## 💾 Bazy Danych

### UserOne (main_backend)
```sql
CREATE TABLE user_one (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255),
    age VARCHAR(255),
    city VARCHAR(255)
);
```

### UserTwo (service_backend)
```sql
CREATE TABLE user_two (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255),
    age VARCHAR(255),
    city VARCHAR(255)
);
```

### TaskResult (main_backend)
```sql
CREATE TABLE task_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(255) UNIQUE,
    status VARCHAR(50),
    result VARCHAR(1000),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 🔧 Migracje Bazy Danych

Każdy backend ma system migracji z Makefile:

#### Main Backend
```bash
cd main_backend

# Uruchomienie migracji (tworzenie tabel)
make migrate-up

# Rollback migracji (usuwanie tabel)
make migrate-down
```

#### Service Backend
```bash
cd service_backend

# Uruchomienie migracji (tworzenie tabel)
make migrate-up

# Rollback migracji (usuwanie tabel)
make migrate-down
```

## 🔌 API Endpoints

### Main Backend (port 3000)

#### Użytkownicy
- **POST** `/users` - Tworzy użytkownika (UserOne) i wysyła zadanie Celery
- **GET** `/users/collection` - Pobiera listę wszystkich użytkowników (UserOne)
- **PATCH** `/users/update/{user_id}` - Aktualizuje użytkownika (UserOne)
- **DELETE** `/users/delete/{user_id}` - Usuwa użytkownika (UserOne)

#### Zadania
- **GET** `/tasks/collection` - Pobiera listę zadań Celery
- **GET** `/task/{task_id}` - Sprawdza status zadania Celery

#### Test
- **GET** `/hello` - Test endpoint

### Service Backend (port 4000)

#### Test
- **GET** `/hello` - Test endpoint

### Przykład użycia:

```bash
# Tworzenie użytkownika
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jan",
    "lastname": "Kowalski",
    "email": "jan@example.com",
    "age": "30",
    "city": "Warszawa"
  }'

# Sprawdzenie statusu zadania
curl http://localhost:3000/task/{task_id}

# Pobranie listy użytkowników
curl http://localhost:3000/users/collection
```

## ⚡ Celery - System Zadań

### Konfiguracja
- **Broker**: RabbitMQ (pyamqp://guest:guest@rabbitmq:5672//)
- **Backend**: Redis (redis://redis:6379/0)
- **Strefa czasowa**: Europe/Warsaw

### Zadania Celery

#### 1. `main_create_user_task`
- Tworzy użytkownika w bazie UserOne
- Wysyła komunikat do RabbitMQ o utworzeniu użytkownika
- Lokalizacja: `main_backend/tasks/create.py`

#### 2. `main_update_user_task`
- Aktualizuje użytkownika w bazie UserOne
- Wysyła komunikat do RabbitMQ o aktualizacji użytkownika
- Lokalizacja: `main_backend/tasks/update.py`

#### 3. `main_delete_user_task`
- Usuwa użytkownika z bazy UserOne
- Wysyła komunikat do RabbitMQ o usunięciu użytkownika
- Lokalizacja: `main_backend/tasks/delete.py`

### Monitorowanie zadań Celery
```bash
# Logi worker'a Celery
docker logs monorepo-celery_worker-1 -f

# Status zadań przez API
curl http://localhost:3000/task/{task_id}
```

## 🐰 RabbitMQ - System Komunikatów

### Konfiguracja
- **Host**: rabbitmq:5672
- **Credentials**: guest/guest
- **Queue**: `user.sync` (durable)
- **Panel zarządzania**: http://localhost:15672

### Format komunikatów
```json
{
  "action": "create|update|delete",
  "user_data": {
    "id": "uuid",
    "name": "string",
    "lastname": "string",
    "email": "string",
    "age": "string",
    "city": "string"
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### Publisher (main_backend)
- **Lokalizacja**: `main_backend/messaging/publisher.py`
- **Funkcje**:
  - `publish_user_created(user_data)`
  - `publish_user_updated(user_data)`
  - `publish_user_deleted(email)`

### Consumer (service_backend)
- **Lokalizacja**: `service_backend/messaging/consumer.py`
- **Funkcjonalność**: Automatyczne przetwarzanie komunikatów i aktualizacja bazy UserTwo

### Monitorowanie RabbitMQ
```bash
# Logi consumer'a
docker logs monorepo-service_consumer-1 -f

# Panel zarządzania RabbitMQ
# http://localhost:15672 (guest/guest)
```

## 🔄 Przepływ Danych

### Tworzenie użytkownika
1. **Frontend** → **POST** `/users` → main_backend
2. Handler uruchamia zadanie Celery `main_create_user_task`
3. Zadanie Celery:
   - Zapisuje użytkownika do bazy UserOne
   - Wysyła komunikat do RabbitMQ
4. Consumer RabbitMQ:
   - Odbiera komunikat
   - Zapisuje użytkownika do bazy UserTwo

### Aktualizacja użytkownika
1. **Frontend** → **PATCH** `/users/update/{user_id}` → main_backend
2. Handler uruchamia zadanie Celery `main_update_user_task`
3. Zadanie Celery:
   - Aktualizuje użytkownika w bazie UserOne
   - Wysyła komunikat do RabbitMQ
4. Consumer RabbitMQ:
   - Odbiera komunikat
   - Aktualizuje użytkownika w bazie UserTwo (wyszukuje po email)

### Usuwanie użytkownika
1. **Frontend** → **DELETE** `/users/delete/{user_id}` → main_backend
2. Handler uruchamia zadanie Celery `main_delete_user_task`
3. Zadanie Celery:
   - Usuwa użytkownika z bazy UserOne
   - Wysyła komunikat do RabbitMQ
4. Consumer RabbitMQ:
   - Odbiera komunikat
   - Usuwa użytkownika z bazy UserTwo (wyszukuje po email)

## 📊 Logi i Monitoring

### Gdzie znajdziesz logi:

```bash
# Frontend
docker logs frontend -f

# Główny backend
docker logs backend_main -f

# Service backend
docker logs backend_service -f

# Celery worker
docker logs monorepo-celery_worker-1 -f

# RabbitMQ consumer
docker logs monorepo-service_consumer-1 -f

# Wszystkie serwisy naraz
docker-compose logs -f
```

### Bazy danych
```bash
# Połączenie z bazą main
docker exec -it postgres_main psql -U postgres -d main_db

# Połączenie z bazą service
docker exec -it postgres_service psql -U postgres -d service_db
```

## 🛠️ Troubleshooting

### Problem z połączeniem do RabbitMQ
```bash
# Restart consumer'a
docker-compose restart service_consumer

# Sprawdź logi RabbitMQ
docker logs rabbitmq
```

### Problem z Celery
```bash
# Restart worker'a
docker-compose restart celery_worker

# Sprawdź połączenie z Redis
docker exec -it redis redis-cli ping
```

### Problem z bazami danych
```bash
# Sprawdź status baz
docker-compose ps | grep postgres

# Restart bazy danych
docker-compose restart postgres_main postgres_service
```

### Problem z Frontend
```bash
# Sprawdź logi frontend'u
docker logs frontend -f

# Restart frontend'u
docker-compose restart frontend

# Sprawdź czy Vite nasłuchuje na właściwym hoście
# Frontend powinien być dostępny na http://localhost:5173
```

## 📁 Struktura Projektu

```
MonoRepo/
├── frontend/                     # Aplikacja Vue.js
│   ├── src/
│   │   ├── components/          # Komponenty Vue
│   │   ├── api/                 # API client
│   │   ├── types/               # Definicje TypeScript
│   │   └── App.vue              # Główny komponent
│   ├── Dockerfile               # Obraz Docker dla frontend'u
│   └── package.json             # Zależności Node.js
├── main_backend/                 # Główny backend (REST API)
│   ├── handler/                 # Endpointy API
│   ├── repository/              # Operacje na bazie danych
│   ├── tasks/                   # Zadania Celery
│   ├── messaging/               # Publisher RabbitMQ
│   ├── database/                # Modele i połączenie z bazą
│   ├── dockerfiles/             # Pliki Docker dla migracji
│   ├── main.py                  # Aplikacja FastAPI
│   ├── celery_app.py           # Konfiguracja Celery
│   └── makefile                 # Komendy migracji i uruchamiania
├── service_backend/              # Backend z consumer'em RabbitMQ
│   ├── repository/              # Operacje na bazie danych
│   ├── messaging/               # Consumer RabbitMQ
│   ├── database/                # Modele i połączenie z bazą
│   ├── dockerfiles/             # Pliki Docker dla migracji
│   ├── main.py                  # Aplikacja FastAPI
│   └── makefile                 # Komendy migracji i uruchamiania
├── docker-compose.yml            # Konfiguracja wszystkich serwisów
└── README.md                     # Ta dokumentacja
```

## ✨ Kluczowe Cechy

✅ **Kompletna aplikacja webowa** - Frontend Vue.js z TypeScript
✅ **Asynchroniczne przetwarzanie** - Celery worker'y
✅ **Komunikacja między serwisami** - RabbitMQ
✅ **Automatyczna synchronizacja baz** - Consumer RabbitMQ
✅ **Monitoring zadań** - Status API Celery
✅ **Separacja kontenerów** - Docker Compose
✅ **Obsługa błędów** - Retry logic w publisher'ze
✅ **Real-time logi** - Osobne kontenery dla lepszego debugowania
✅ **System migracji** - Makefile commands dla obu backend'ów
✅ **CORS configuration** - Prawidłowa komunikacja frontend ↔ backend
✅ **TypeScript support** - Silne typowanie w całej aplikacji

## 🏃‍♂️ Quick Start

1. **Uruchom wszystko**:
   ```bash
   docker-compose up -d
   ```

2. **Otwórz frontend**: http://localhost:5173

3. **Utwórz użytkownika** przez formularz w przeglądarce

4. **Sprawdź synchronizację** - użytkownik powinien pojawić się w obu bazach danych

5. **Monitoruj zadania** w panelu aplikacji

## 📧 Kontakt

Projekt stworzony do demonstracji architektury mikrousług z pełnym frontend'em Vue.js i synchronizacją baz danych.