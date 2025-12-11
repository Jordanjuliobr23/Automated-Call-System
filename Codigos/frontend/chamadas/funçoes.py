from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, StreamingResponse 
import uuid, io, time
from datetime import datetime, timedelta
import qrcode
import requests
from typing import Optional



app = FastAPI()
TOKENS = {}

TIME = 180 
URL = "http://localhost:8000/aluno/"


@app.get("/gera_qr")
async def gera_qr():
    token = str(uuid.uuid4())
    agora = datetime.utcnow()
    expira = agora + timedelta(seconds=TIME)


    suap_url = f"{URL}/accounts/login/"
    
    TOKENS[token] = {
        "crie": agora, 
        "expira": expira, 
        "use": False, 
        "used_at": None,
        "auth_url": URL,  
        "user_data": None,
        "access_token": None,
        "authenticated": False  
    }
    
    
    png = qrcode.make(URL)
    buf = io.BytesIO()
    png.save(buf, format="PNG")
    buf.seek(0)

    return {
        "token": token, 
        "auth_url": URL,
        "qr_code_url": f"http://localhost:8001/qr_image/{token}"
    }


@app.get("/qr_image/{token}")
async def qr_image(token: str):
    dados = TOKENS.get(token)
    if not dados:
        raise HTTPException(status_code=404, detail="Token não encontrado")

  
    png = qrcode.make(dados["auth_url"])
    buf = io.BytesIO()
    png.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")