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

    # MANTENHA os mesmos nomes em todos os lugares
    TOKENS[token] = {"crie": agora, "expira": expira, "use": False, "used_at": None}
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

    # CORRIJA: use "validade" (igual ao /gera_qr)
    validade_url = f'http://auth.presenca.local/validade/{token}'
    png = qrcode.make(validade_url)
    buf = io.BytesIO()
    png.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/validade/{token}")
async def validade_token(request: Request, token: str):
    agora = datetime.utcnow()

    registros = TOKENS.get(token)
    if not registros:
        raise HTTPException(status_code=404, detail="QR inválido!")

    # USE os mesmos nomes: "use" e "expira"
    if registros["use"]:
        raise HTTPException(status_code=400, detail="QR já utilizado!")

    if agora > registros["expira"]:  # mude para "expira"
        registros["use"] = True
        raise HTTPException(status_code=400, detail="QR expirado!") 
    
    registros["use"] = True
    registros["used_at"] = agora
    return {"message": "Token validado com sucesso!"}  # adicione return

@app.get('/_tokens')
async def lista_tokens():
    saida = {}
    for k, v in TOKENS.items():
        saida[k] = {
            # USE os mesmos nomes do dicionário
            "crie": v["crie"].isoformat(),
            "expira": v["expira"].isoformat(),
            "use": v["use"],
            "used_at": v["used_at"].isoformat() if v["used_at"] else None
        }
    return saida
