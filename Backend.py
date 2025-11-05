
from fastapi import FastAPI, HTTPException, Request 
from fastapi.responses import RedirectResponse, StreamingResponse 
import uuid, io, time
from datetime import datetime, timedelta
import qrcode

app = FastAPI()
TOKENS = {}

TIME= 180 
LOGIN = "https://suap.ifrn.edu.br/accounts/login/?next=/api/"




