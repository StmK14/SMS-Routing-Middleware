from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "¡API funcionando correctamente!"}

#Montar archivos estáticos (favicon y otros posibles)
app.mount("/static", StaticFiles(directory="sms_router/static"), name="static")

#Ruta directa para el favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("sms_router/static/favicon.ico")

class SMSRequest(BaseModel):
    to: str
    message: str

@app.post("/send-sms")
def send_sms(sms: SMSRequest):
    country_prefix = sms.to[:3]

    try:
        if country_prefix == "+34":
            # España → usar Twilio
            response = requests.post(
                "https://api.twilio.com/send",  # Reemplazar con endpoint real
                json={"to": sms.to, "message": sms.message},
                headers={"Authorization": f"Bearer {os.getenv('TWILIO_TOKEN')}"}
            )
        elif country_prefix == "+1":
            # EE.UU. → usar Azure
            response = requests.post(
                "https://your-azure-sms-endpoint.com/send",  # Reemplazar con endpoint real
                json={"to": sms.to, "message": sms.message},
                headers={"Authorization": f"Bearer {os.getenv('AZURE_TOKEN')}"}
            )
        else:
            # Otros → usar Infobip
            response = requests.post(
                "https://api.infobip.com/send",  # Reemplazar con endpoint real
                json={"to": sms.to, "message": sms.message},
                headers={"Authorization": f"App {os.getenv('INFOBIP_TOKEN')}"}
            )

        if response.status_code == 200:
            return {"status": "OK", "provider_response": response.json()}
        else:
            raise HTTPException(status_code=500, detail="Provider error")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
