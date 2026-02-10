from django.urls import path
from .views import registrar_aluno, professor_login, listar_aulas, listar_alunos
from .views import DiarioList, ChamadaList
from .views import (gerar_chave,mostrar_qr,expirar_chave,registrar_aluno)

urlpatterns = [
    #path("", IndexView.as_view(), name="index"),
    path("professor/login", professor_login, name="professor-login"),
    path("professor/diarios", DiarioList.as_view(), name="listar-diarios"),
    path("professor/diarios/<int:diario_id>/aulas/", listar_aulas, name="listar-aulas"),
    path("professor/diarios/<int:diario_id>/alunos/", listar_alunos, name="listar-alunos"),
    path("professor/chamadas", ChamadaList.as_view(), name="listar-chamadas"),
    
    path("gerar/<int:aula_id>/", gerar_chave, name="gerar_chave"),
    path("qr/<int:aula_id>/<str:codigo>/", mostrar_qr, name="mostrar_qr"),
    path("chave/<str:codigo>/expirar/", expirar_chave, name="expirar_chave"),
    path("aluno/<str:codigo>/", registrar_aluno, name="registrar_aluno"),
]