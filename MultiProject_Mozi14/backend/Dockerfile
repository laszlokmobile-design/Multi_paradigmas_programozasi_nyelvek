# ===== Backend Dockerfile =====
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y build-essential

# Work directory a konténeren belül
WORKDIR /app

# Másoljuk a teljes backend mappát (Docker build kontextus: backend)
COPY . /app

# Másoljuk külön a movies.db-t is (ha nincs benne a .dockerignore-ban)
#COPY movies.db /app/movies.db

# Python path beállítása, hogy a backend root csomagként legyen elérhető
ENV PYTHONPATH=/app

# Make start.sh executable
RUN chmod +x /app/start.sh

# Upgrade pip és install
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port
EXPOSE 8000

# Start server + migráció
#CMD ["sh", "-c", "python backend/migrate_db.py && uvicorn backend.main:app --host 0.0.0.0 --port $PORT"]
CMD ["sh", "/app/start.sh"]






