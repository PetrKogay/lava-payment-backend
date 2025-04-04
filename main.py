from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import hashlib
import hmac
import os

app = FastAPI()

LAVA_API_KEY = os.getenv("LAVA_API_KEY")
LAVA_SHOP_ID = os.getenv("LAVA_SHOP_ID")
LAVA_WEBHOOK_SECRET = os.getenv("LAVA_WEBHOOK_SECRET")


@app.get("/")
async def root():
    return {"message": "Lava Payment Backend is running"}


@app.post("/lava/callback")
async def lava_callback(request: Request):
    body = await request.body()
    headers = request.headers

    received_sign = headers.get("Sign", "")

    if not received_sign:
        return JSONResponse(status_code=400, content={"error": "No sign header"})

    expected_sign = hmac.new(
        LAVA_WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()

    if received_sign != expected_sign:
        return JSONResponse(status_code=403, content={"error": "Invalid signature"})

    data = await request.json()
    print("💰 Успешная оплата:", data)
    return {"status": "ok"}
