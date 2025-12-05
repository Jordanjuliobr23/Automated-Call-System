from django.urls import path
from .views import *

urlpatterns = [
    #path("", IndexView.as_view(), name="index"),
    path("aluno/", registrar_aluno, name="aluno"),
    path("professor/", ProfessorCreate.as_view(), name="professor"),
    
]