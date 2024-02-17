#!/bin/bash
poetry run alembic --config /app/migrations/alembic.ini upgrade head

echo 'starting server'
poetry run sentinel -v --structured $*
