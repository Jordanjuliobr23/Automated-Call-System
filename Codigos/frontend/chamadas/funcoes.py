import qrcode, io, base64

URL = f"http://192.168.0.12:8000/aluno/"

def qr_image(codigo: str):  
    img = qrcode.make(f"{URL}{codigo}")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")