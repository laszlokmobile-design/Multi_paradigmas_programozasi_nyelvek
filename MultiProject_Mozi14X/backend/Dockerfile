# ===== Backend Dockerfile =====
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y build-essential

# Work directory a konténeren belül
WORKDIR /app


# Copy everything from the current directory (backend)
#COPY . .
COPY . /app
# Python path beállítása, hogy a backend root csomagként legyen elérhető
ENV PYTHONPATH=/app

# Upgrade pip és install
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
