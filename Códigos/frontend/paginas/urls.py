from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("professor/", ProfessorView.as_view(), name="professor"),
]