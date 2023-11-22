# The manage.py command
MANAGE_PY=python manage.py
CELERY_MODULE=task_ai.app.handlers


# Default target: start the development server
.PHONY: install
install:
	pip install -r requirements.txt


# Default target: start the development server
.PHONY: run
run:
	$(MANAGE_PY) runserver

# Target for making database migrations
.PHONY: migrations
migrations:
	$(MANAGE_PY) makemigrations

# Target for applying database migrations
.PHONY: migrate
migrate:
	$(MANAGE_PY) migrate

# Target for running tests
.PHONY: test
test:
	$(MANAGE_PY) test

# Target for starting a Django shell
.PHONY: shell
shell:
	$(MANAGE_PY) shell

.PHONY: format-check
format-check:
	black --check .

.PHONY: format-fix
format-fix:
	black .

.PHONY: lint
lint:
	pylint --rcfile=.pylintrc task_ai

.PHONY: clean
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-database
clean-database:
	rm -f db.sqlite3
	make migrations
	make migrate

.PHONY: celery
celery:
	celery -A $(CELERY_MODULE) worker