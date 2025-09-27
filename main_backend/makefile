install_dependencies:
	pip install -r requirements.txt

clean_cache:
	find . -name "__pycache__" -exec rm -rf {} + || rmdir /s /q __pycache__
	find . -name "*.pyc" -delete || del /s /q *.pyc

lint:
	flake8 .

run_worker:
	celery -A celery_app.celery_app worker --loglevel=info

run_app:
	uvicorn main:app_main --reload --log-level debug --port 3000

# Database Migration Commands
migrate-up:
	cd dockerfiles/migration_db && docker-compose -f docker-compose.migration.yml run --rm --build migration bash ./db_migration_up.sh

migrate-down:
	cd dockerfiles/migration_db && docker-compose -f docker-compose.migration.yml run --rm --build migration bash ./db_migration_down.sh
