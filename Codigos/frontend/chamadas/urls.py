from django.urls import path
from .views import registrar_aluno, ProfessorCreate
from .views import DisciplinaList, DiarioList, AulaList, AlunoList

urlpatterns = [
    #path("", IndexView.as_view(), name="index"),
    path("aluno/", registrar_aluno, name="aluno"),
    path("professor/", ProfessorCreate.as_view(), name="professor"),
    path("professor/listar/disciplina", DisciplinaList.as_view(), name="listar-disciplina"),
    path("professor/listar/diario", DiarioList.as_view(), name="listar-diario"),
    path("professor/listar/aula", AulaList.as_view(), name="listar-aula"),
    path("professor/listar/aluno", AlunoList.as_view(), name="listar-aluno"),
]