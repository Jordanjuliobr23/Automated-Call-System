#teste2
from fastapi import FastAPI, HTTPException, Request 
from fastapi.responses import RedirectResponse, StreamingResponse 
import uuid, io, time
from datetime import datetime, timedelta
import qrcode

app = FastAPI()
TOKENS = {}

TIME= 180 
LOGIN = "https://suap.ifrn.edu.br/accounts/login/?next=/api/"

@app.get("/gera_qr")
async def gera_qr():
    token = str(uuid.uuid4())
    agora = datetime.utcnow()
    expira = agora + timedelta(seconds=TIME)

    TOKENS[token] = {"crie": agora, "expira": expira, "use": False}
    validade_url = f"http://auth.presenca.local/validade/{token}"
    
    png = qrcode.make(validade_url)
    buf = io.BytesIO()
    png.save(buf, format="PNG")
    buf.seek(0)

    return {"token": token, "validade_url": validade_url}

@app.get("/qr_image/{token}")
async def qr_image(token: str):
    dados = TOKENS.get(token)
    if not dados:
        raise HTTPException(status_code=404, detail="Token não encontrado")

    validade_url = f'http://auth.presenca.local/validate/{token}'
    png = qrcode.make(validade_url)
    buf = io.BytesIO()
    png.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@app.get("/validate/{token}")
async def validade_token(request: Request, token: str):
    agora = datetime.utcnow()

    registros = TOKENS.get(token)
    if not registros:
        raise HTTPException(status_code=404, detail="QR inválido!")

    if registros["used"]:
        raise HTTPException(status_code=400, detail="QR já utilizado!")

    if agora > registros["expires_at"]:
        registros["used"] = True
        raise HTTPException(status_code=400, detail="QR expirado!") 
    
    registros["used"] = True
    registros["used_at"] = agora

@app.get('/_tokens')
async def lista_tokens():
    saida = {}
    for k, v in TOKENS.items():
        saida[k] = {
            "created": v["created_at"].isoformat(),
            "expires_at": v["expires_at"].isoformat(),
            "used": v["used"],
            "used_at": v["used_at"].isoformat() if v["used_at"] else None
        }
    return saida
