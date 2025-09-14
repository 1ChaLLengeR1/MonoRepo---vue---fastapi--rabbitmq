# MonoRepo - System Synchronizacji Baz Danych

Projekt demonstracyjny systemu mikrousBug z synchronizacj baz danych przy u|yciu RabbitMQ i Celery.

## =� Opis Projektu

Prosty system skBadajcy si z dw�ch backend'�w, kt�re zarzdzaj r�|nymi bazami danych u|ytkownik�w:
- **main_backend** - zarzdza baz `UserOne` przez REST API
- **service_backend** - zarzdza baz `UserTwo` przez komunikaty RabbitMQ

GB�wny cel: **aktualizacja bazy UserTwo odbywa si automatycznie poprzez RabbitMQ przy ka|dej operacji CRUD na UserOne**.

## <� Architektura Systemu

```
                                                           
   main_backend          RabbitMQ          service_backend 
   (REST API)       �   (Messaging)      �   (Consumer)    
                                                           
   PostgreSQL             Redis              PostgreSQL    
   (UserOne)             (Celery)            (UserTwo)     
                                                           
```

## =� Jak Uruchomi Projekt

### Wymagania
- Docker
- Docker Compose

### Uruchomienie
```bash
# Klonowanie repozytorium
git clone <repo-url>
cd MonoRepo

# Uruchomienie wszystkich serwis�w
docker-compose up -d

# Sprawdzenie statusu kontener�w
docker-compose ps
```

## =3 Serwisy Docker

| Serwis | Port | Opis |
|--------|------|------|
| **backend_main** | 3000 | FastAPI - gB�wny backend z REST API |
| **backend_service** | 4000 | FastAPI - serwis z consumerem RabbitMQ |
| **celery_worker** | - | Worker Celery do przetwarzania zadaD |
| **service_consumer** | - | Osobny consumer RabbitMQ |
| **postgres_main** | 5450 | Baza danych dla UserOne |
| **postgres_service** | 5434 | Baza danych dla UserTwo |
| **rabbitmq** | 5672, 15672 | Message broker (panel: http://localhost:15672) |
| **redis** | 6379 | Backend dla Celery |

## =� Bazy Danych

### UserOne (main_backend)
```sql
CREATE TABLE user_one (
    id UUID PRIMARY KEY,
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
    id UUID PRIMARY KEY,
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
    id UUID PRIMARY KEY,
    task_id VARCHAR(255) UNIQUE,
    status ENUM('pending', 'running', 'success', 'failure'),
    result VARCHAR(1000),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## = API Endpoints

### Main Backend (port 3000)

#### U|ytkownicy
- **POST** `/users` - Tworzy u|ytkownika (UserOne) i wysyBa zadanie Celery
- **GET** `/users/collection` - Pobiera list wszystkich u|ytkownik�w (UserOne)
- **PATCH** `/users/update/{user_id}` - Aktualizuje u|ytkownika (UserOne)
- **DELETE** `/users/delete/{user_id}` - Usuwa u|ytkownika (UserOne)

#### Zadania Celery
- **GET** `/task/{task_id}` - Sprawdza status zadania Celery

#### Test
- **GET** `/hello` - Test endpoint

### Service Backend (port 4000)

#### Test
- **GET** `/hello` - Test endpoint

### PrzykBad u|ycia:

```bash
# Tworzenie u|ytkownika
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

# Pobranie listy u|ytkownik�w
curl http://localhost:3000/users/collection
```

## � Celery - System ZadaD

### Konfiguracja
- **Broker**: RabbitMQ (pyamqp://guest:guest@rabbitmq:5672//)
- **Backend**: Redis (redis://redis:6379/0)
- **Strefa czasowa**: Europe/Warsaw

### Zadania Celery

#### 1. `main_create_user_task`
- Tworzy u|ytkownika w bazie UserOne
- WysyBa komunikat do RabbitMQ o utworzeniu u|ytkownika
- Lokalizacja: `main_backend/tasks/create.py`

#### 2. `main_update_user_task`
- Aktualizuje u|ytkownika w bazie UserOne
- WysyBa komunikat do RabbitMQ o aktualizacji u|ytkownika
- Lokalizacja: `main_backend/tasks/update.py`

#### 3. `main_delete_user_task`
- Usuwa u|ytkownika z bazy UserOne
- WysyBa komunikat do RabbitMQ o usuniciu u|ytkownika
- Lokalizacja: `main_backend/tasks/delete.py`

### Monitorowanie zadaD Celery
```bash
# Logi worker'a Celery
docker logs monorepo-celery_worker-1 -f

# Status zadaD przez API
curl http://localhost:3000/task/{task_id}
```

## =0 RabbitMQ - System Komunikat�w

### Konfiguracja
- **Host**: rabbitmq:5672
- **Credentials**: guest/guest
- **Queue**: `user.sync` (durable)
- **Panel zarzdzania**: http://localhost:15672

### Format komunikat�w
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
- **Funkcjonalno[**: Automatyczne przetwarzanie komunikat�w i aktualizacja bazy UserTwo

### Monitorowanie RabbitMQ
```bash
# Logi consumer'a
docker logs monorepo-service_consumer-1 -f

# Panel zarzdzania RabbitMQ
# http://localhost:15672 (guest/guest)
```

## = PrzepByw Danych

### Tworzenie u|ytkownika
1. **POST** `/users` � main_backend
2. Handler uruchamia zadanie Celery `main_create_user_task`
3. Zadanie Celery:
   - Zapisuje u|ytkownika do bazy UserOne
   - WysyBa komunikat do RabbitMQ
4. Consumer RabbitMQ:
   - Odbiera komunikat
   - Zapisuje u|ytkownika do bazy UserTwo

### Aktualizacja u|ytkownika
1. **PATCH** `/users/update/{user_id}` � main_backend
2. Handler uruchamia zadanie Celery `main_update_user_task`
3. Zadanie Celery:
   - Aktualizuje u|ytkownika w bazie UserOne
   - WysyBa komunikat do RabbitMQ
4. Consumer RabbitMQ:
   - Odbiera komunikat
   - Aktualizuje u|ytkownika w bazie UserTwo (wyszukuje po email)

### Usuwanie u|ytkownika
1. **DELETE** `/users/delete/{user_id}` � main_backend
2. Handler uruchamia zadanie Celery `main_delete_user_task`
3. Zadanie Celery:
   - Usuwa u|ytkownika z bazy UserOne
   - WysyBa komunikat do RabbitMQ
4. Consumer RabbitMQ:
   - Odbiera komunikat
   - Usuwa u|ytkownika z bazy UserTwo (wyszukuje po email)

## =� Logi i Monitoring

### Gdzie znajdziesz logi:

```bash
# GB�wny backend
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
# PoBczenie z baz main
docker exec -it postgres_main psql -U postgres -d main_db

# PoBczenie z baz service
docker exec -it postgres_service psql -U postgres -d service_db
```

## =� Troubleshooting

### Problem z poBczeniem do RabbitMQ
```bash
# Restart consumer'a
docker-compose restart service_consumer

# Sprawdz logi RabbitMQ
docker logs rabbitmq
```

### Problem z Celery
```bash
# Restart worker'a
docker-compose restart celery_worker

# Sprawdz poBczenie z Redis
docker exec -it redis redis-cli ping
```

### Problem z bazami danych
```bash
# Sprawdz status baz
docker-compose ps | grep postgres

# Restart bazy danych
docker-compose restart postgres_main postgres_service
```

## =� Struktura Projektu

```
MonoRepo/
   main_backend/                 # GB�wny backend (REST API)
      handler/                  # Endpointy API
      repository/               # Operacje na bazie danych
      tasks/                    # Zadania Celery
      messaging/                # Publisher RabbitMQ
      database/                 # Modele i poBczenie z baz
      main.py                   # Aplikacja FastAPI
      celery_app.py            # Konfiguracja Celery
   service_backend/              # Backend z consumer'em RabbitMQ
      repository/               # Operacje na bazie danych
      messaging/                # Consumer RabbitMQ
      database/                 # Modele i poBczenie z baz
      main.py                   # Aplikacja FastAPI
   docker-compose.yml            # Konfiguracja wszystkich serwis�w
   README.md                     # Ta dokumentacja
```

## <� Kluczowe Cechy

 **Asynchroniczne przetwarzanie** - Celery worker'y
 **Komunikacja midzy serwisami** - RabbitMQ
 **Automatyczna synchronizacja baz** - Consumer RabbitMQ
 **Monitoring zadaD** - Status API Celery
 **Separacja kontener�w** - Docker Compose
 **ObsBuga bBd�w** - Retry logic w publisher'ze
 **Real-time logi** - Osobne kontenery dla lepszego debugowania

## =h
=� Autorzy

Projekt stworzony do demonstracji architektury mikrousBug z synchronizacj baz danych.
