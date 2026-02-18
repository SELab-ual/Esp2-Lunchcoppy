
# Amazing Lunch - Sprint 1 Prototype

## Prerequisites
- Docker and Docker Compose installed
- Open ports 80 and 443 available (or adjust compose ports)

## Setup (dev)
1. Clone repository.
2. Generate self-signed certs:




Run befor compose
```
mkdir -p nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/privkey.pem \
  -out nginx/certs/fullchain.pem \
  -subj "/CN=localhost"
```

```mkdir -p nginx/certs openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/certs/privkey.pem -out nginx/certs/fullchain.pem -subj "/CN=localhost"
```


EN windows

New-Item -ItemType Directory -Force -Path "nginx/certs"

3. Copy `.env.example` to `.env` and adjust if needed.
4. Start services:


```
docker-compose up --build
```

5. Open `https://localhost` in your browser (accept the self-signed cert).

## Test accounts and seed data
- A seeded user exists: **username** `tester` **password** `password`.
- Seeded restaurants are created on startup.

## Notes and next steps
- Replace self-signed certs with a proper certificate manager for production.
- Move `SECRET_KEY` to a secrets manager.
- Add DB backups, migrations (Alembic), and production WSGI server (Gunicorn + Uvicorn workers).



### NOTAR ISA ajuste en requirements.txt

el original
```
fastapi==0.95.2
uvicorn[standard]==0.22.0
sqlmodel==0.0.8
psycopg2-binary==2.9.7
passlib[bcrypt]==1.7.4
python-jose==3.3.0
pydantic==1.10.7
python-dotenv==1.0.0
```

Hubo que cambiar librerías añadiendo -- cambia dependencias
 
```
fastapi==0.95.2
uvicorn[standard]==0.22.0
sqlmodel==0.0.8
psycopg2-binary==2.9.7
passlib[bcrypt]==1.7.4
python-jose==3.3.0
pydantic==1.10.7
python-dotenv==1.0.0


bcrypt==4.0.1
```
