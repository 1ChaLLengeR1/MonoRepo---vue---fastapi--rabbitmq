#!/bin/bash

ENV_FILE="../.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Plik środowiskowy $ENV_FILE nie istnieje!"
    sleep 5
    exit 1
fi

source "$ENV_FILE"

if [ -z "$DB_HOST_2" ] || [ -z "$DB_PORT_2" ] || [ -z "$DB_USER_2" ] || [ -z "$DB_PASSWORD_2" ] || [ -z "$DB_DBNAME_2" ]; then
    echo "Wszystkie zmienne środowiskowe muszą być ustawione w pliku local.env"
    sleep 10
    exit 1
fi

if [ ! -f ../database/database_up.sql ]; then
    echo "Plik ../database/database_up.sql nie istnieje!"
    sleep 10
    exit 1
fi


export PGPASSWORD="$DB_PASSWORD_SCRIPT_2"
psql -h "$DB_HOST_2" -U "$DB_USER_2" -d "$DB_DBNAME_2" -p "$DB_PORT_2" -f "../database/database_up.sql"


if [ $? -eq 0 ]; then
    echo "Migracja zakończona pomyślnie!"
else
    echo "Błąd podczas migracji."
    sleep 10
    exit 1
fi

echo "Skrypt zakończy się za 5 sekund..."
sleep 5

