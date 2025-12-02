from django.db import models

# Create your models here.

class Professor(models.Model):
    matricula = models.CharField(max_length=14, verbose_name="Matrícula", primary_key=True)
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.nome}, {self.matricula}"
    
class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=20)
    curso = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome}, {self.sigla}"

class Diario(models.Model):
    id = models.AutoField(primary_key=True)
    turno = models.CharField(max_length=30)

    professor = models.ForeignKey(Professor, on_delete=models.PROTECT)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.professor}, {self.turno}, {self.disciplina}"