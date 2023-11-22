MANAGE_PY=python manage.py
CELERY_MODULE=task_ai.app.handlers

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run:
	$(MANAGE_PY) runserver

.PHONY: migrations
migrations:
	$(MANAGE_PY) makemigrations

.PHONY: migrate
migrate:
	$(MANAGE_PY) migrate

.PHONY: test
test:
	$(MANAGE_PY) test

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