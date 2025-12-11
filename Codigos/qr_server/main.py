from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse, StreamingResponse 
import uuid, io, time
from datetime import datetime, timedelta
import qrcode
import requests
from typing import Optional

#openssl rand -hex 4

app = FastAPI()
TOKENS = {}

TIME = 180 
url = "http://localhost:8000/aluno/"


@app.get("/gera_qr")
async def gera_qr():
    token = str(uuid.uuid4())
    agora = datetime.utcnow()
    expira = agora + timedelta(seconds=TIME)


    
    
    TOKENS[token] = {
        "crie": agora, 
        "expira": expira, 
        "use": False, 
        "used_at": None,
        "auth_url": url,  
        "user_data": None,
        "access_token": None,
        "authenticated": False  
    }
    
    
    png = qrcode.make(url)
    buf = io.BytesIO()
    png.save(buf, format="PNG")
    buf.seek(0)

    return {
        "token": token, 
        "auth_url": url,
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


@app.get("/validade/{token}")
async def validade_token(token: str):

    agora = datetime.utcnow()

    registros = TOKENS.get(token)
    if not registros:
        raise HTTPException(status_code=404, detail="QR inválido!")

    if registros["use"]:
        raise HTTPException(status_code=400, detail="QR já utilizado!")

    if agora > registros["expira"]:  
        registros["use"] = True
        raise HTTPException(status_code=400, detail="QR expirado!") 
    
 
    if registros["authenticated"]:
        registros["use"] = True
        return {
            "status": "autenticado",
            "user": registros["user_data"],
            "message": "Usuário autenticado com sucesso!"
        }
    else:
        return {
            "status": "pendente",
            "message": "Aguardando autenticação...",
            "auth_url": registros["auth_url"]
        }


@app.get("/simular_auth/{token}")
async def simular_auth(token: str, username: str = "usuario_teste"):
    dados = TOKENS.get(token)
    if not dados:
        raise HTTPException(status_code=404, detail="Token não encontrado")
    
    dados["authenticated"] = True
    dados["user_data"] = {
        "username": username,
        "name": "Usuário de Teste",
        "email": f"{username}@ifrn.edu.br"
    }
    dados["used_at"] = datetime.utcnow()
    dados["use"] = True
    
    return {
        "message": "Autenticação simulada com sucesso!",
        "user": dados["user_data"]
    }

@app.get("/user/{token}")
async def get_user_data(token: str):
    dados = TOKENS.get(token)
    if not dados or not dados["user_data"]:
        raise HTTPException(status_code=404, detail="Token não encontrado ou não autenticado")
    
    return dados["user_data"]

@app.get('/_tokens')
async def lista_tokens():
    saida = {}
    for k, v in TOKENS.items():
        saida[k] = {
            "crie": v["crie"].isoformat(),
            "expira": v["expira"].isoformat(),
            "use": v["use"],
            "used_at": v["used_at"].isoformat() if v["used_at"] else None,
            "user_data": v["user_data"] is not None,
            "authenticated": v["authenticated"]
        }
    return saida

@app.get("/")
async def root():
    return {"message": "Sistema de autenticação via QR Code - SUAP"}


@app.get("/auth/callback")
async def auth_callback(code: str = None, state: str = None):
    return {"message": "Callback do SUAP - Implemente OAuth aqui posteriormente"}
