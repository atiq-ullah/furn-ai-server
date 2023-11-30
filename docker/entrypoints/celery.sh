#!/bin/bash

sh ./docker/entrypoints/shared.sh

exec celery -A task_ai worker --loglevel=info
