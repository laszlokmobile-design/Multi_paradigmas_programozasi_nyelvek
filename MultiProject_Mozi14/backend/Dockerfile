# ===== Backend Dockerfile =====
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y build-essential

# Work directory a konténeren belül
WORKDIR /app

# Másoljuk a backend mappát
COPY backend /app/backend

# Másoljuk a movies.db-t a backend-be
COPY movies.db /app/backend/movies.db

# Python path beállítása, hogy a backend root csomagként legyen elérhető
ENV PYTHONPATH=/app

# Upgrade pip és install
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Expose port
EXPOSE 8000

# Start server + migráció
CMD ["sh", "-c", "python backend/migrate_db.py && uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]



