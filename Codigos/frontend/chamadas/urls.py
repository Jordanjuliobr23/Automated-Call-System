from django.urls import path
from .views import registrar_aluno, registrar_professor
from .views import DisciplinaList, DiarioList, AulaList, AlunoList, ChamadaList
from .views import (gerar_chave,mostrar_qr,expirar_chave,registrar_aluno)

urlpatterns = [
    #path("", IndexView.as_view(), name="index"),
    path("professor/login", registrar_professor, name="professor-login"),
    path("professor/listar/disciplina", DisciplinaList.as_view(), name="listar-disciplina"),
    path("professor/listar/diario", DiarioList.as_view(), name="listar-diario"),
    path("professor/listar/aula", AulaList.as_view(), name="listar-aula"),
    path("professor/listar/aluno", AlunoList.as_view(), name="listar-aluno"),
    path("professor/listar/chamada", ChamadaList.as_view(), name="listar-chamada"),
    
    path("gerar/<int:aula_id>/", gerar_chave, name="gerar_chave"),
    path("qr/<str:codigo>/", mostrar_qr, name="mostrar_qr"),
    path("chave/<str:codigo>/expirar/", expirar_chave, name="expirar_chave"),
    path("aluno/<str:codigo>/", registrar_aluno, name="registrar_aluno"),
]