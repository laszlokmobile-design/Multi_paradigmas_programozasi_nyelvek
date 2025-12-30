#!/bin/sh
# Migráció
python backend/migrate_db.py

# Backend indítása
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
