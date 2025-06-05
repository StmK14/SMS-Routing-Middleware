# SMS Routing Middleware (Azure + Twilio + Infobip)

Este microservicio enruta mensajes SMS según el país del destinatario usando FastAPI. Permite elegir el proveedor SMS adecuado según el prefijo del número.

## 📦 Estructura del proyecto

```
sms_router/
├── main.py
├── .env.example
├── requirements.txt
├── Dockerfile
```

## 🚀 Cómo usar

### 1. Clonar y preparar entorno

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### 2. Crear archivo `.env`

```bash
cp .env.example .env
```

Rellena tus tokens reales de Twilio, Azure y/o Infobip.

### 3. Ejecutar localmente

```bash
uvicorn sms_router.main:app --reload
```

### 4. Probar con curl

```bash
curl -X POST http://localhost:8000/send-sms \
 -H "Content-Type: application/json" \
 -d '{"to": "+34612345678", "message": "Hola"}'
```

### 🐳 Docker

```bash
docker build -t sms-middleware .
docker run --env-file .env -p 8000:8000 sms-middleware
```

---
