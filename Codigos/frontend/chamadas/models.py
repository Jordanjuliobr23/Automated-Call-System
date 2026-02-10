from django.db import models
from django.utils import timezone
import secrets
from datetime import time
from collections import defaultdict

# Bloco Superior até Chamada

class Professor(models.Model):
    matricula = models.CharField(max_length=14, verbose_name="matrícula", unique=True, primary_key=True)
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nome} - {self.matricula}"
    
class Aluno(models.Model):
    matricula = models.CharField(max_length=14, verbose_name="matrícula", unique=True, primary_key=True)
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nome} - {self.matricula}"
    
class Disciplina(models.Model):
    id_suap = models.PositiveIntegerField(primary_key=True, unique=True)
    sigla = models.CharField(max_length=20)
    nome = models.CharField(max_length=150)
    nivel = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.sigla} - {self.nome} - {self.nivel}"

class Diario(models.Model):
    id_suap = models.PositiveIntegerField(primary_key=True, unique=True)

    local = models.CharField(max_length=150)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professores = models.ManyToManyField(Professor,through="ProfessorDiario")
    alunos = models.ManyToManyField(Aluno,through="AlunoDiario")
    
    def __str__(self):
        return f"{self.disciplina}"
    
    def horario_resumido(self):
        HORARIOS_ORDEM = {
            "07:00 - 07:45": "1",
            "07:45 - 08:30": "2",
            "09:00 - 09:45": "3",
            "09:45 - 10:30": "4",
            "10:30 - 11:15": "5",
            "11:15 - 12:00": "6",

            "13:00 - 13:45": "1",
            "13:45 - 14:30": "2",
            "14:30 - 15:15": "3",
            "15:15 - 16:00": "4",
            "16:30 - 17:15": "5",
            "17:15 - 18:00": "6",

            "19:00 - 19:45": "1",
            "19:45 - 20:30": "2",
            "20:40 - 21:25": "3",
            "21:25 - 22:10": "4",
        }

        DIAS = {
            "Domingo": "1",
            "Segunda": "2",
            "Terça": "3",
            "Quarta": "4",
            "Quinta": "5",
            "Sexta": "6",
            "Sábado": "7",
        }

        def identificar_turno(hora_inicio):
            h, m = map(int, hora_inicio.split(":"))
            t = time(h, m)
            if time(7, 0) <= t <= time(12, 0):
                return "M"
            elif time(13, 0) <= t <= time(18, 0):
                return "V"
            elif time(19, 0) <= t <= time(22, 10):
                return "N"

        grupos = defaultdict(list)

        for h in self.horario_set.all():
            dia_codigo = DIAS[h.dia]
            ini, fim = h.horario.split(" - ")
            turno = identificar_turno(ini)
            ordem = HORARIOS_ORDEM[h.horario]

            grupos[(dia_codigo, turno)].append(ordem)

        partes = []
        for (dia, turno), nums in sorted(grupos.items()):
            partes.append(f"{dia}{turno}{''.join(sorted(nums))}")

        return " / ".join(partes)
    
class ProfessorDiario(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    diario = models.ForeignKey(Diario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("professor", "diario")

    def __str__(self):
        return f"{self.professor} - {self.diario}"

class AlunoDiario(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    diario = models.ForeignKey(Diario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("aluno", "diario")

    def __str__(self):
        return f"{self.aluno} - {self.diario}"
    
class Horario(models.Model):
    DIA = (('Domingo','Domingo'),('Segunda','Segunda'),('Terça','Terça'),('Quarta','Quarta'),('Quinta','Quinta'),('Sexta','Sexta'),('Sábado','Sábado'))

    id = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=7, choices=DIA)
    horario = models.CharField(max_length=13)
    diario = models.ManyToManyField(Diario,through="DiarioHorario")

    def __str__(self):
        return f"{self.dia} - {self.horario}"
    
class DiarioHorario(models.Model):
    diario = models.ForeignKey(Diario, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("diario","horario")

    def __str__(self):
        return f"{self.diario} - {self.horario}"
    
class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    etapa = models.IntegerField()
    quantidade = models.IntegerField()
    conteudo = models.TextField(blank=True, null=True)
    
    diario = models.ForeignKey(Diario, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.quantidade} - {self.data.strftime('%d/%m/%Y')} - {self.conteudo}"
    

# Bloco inferior até chamada
    
class Chave(models.Model):
    codigo = models.CharField(max_length=64, primary_key=True, unique=True, verbose_name="Código",default=secrets.token_urlsafe)
    status = models.BooleanField(default=False)
    criadoEm = models.DateTimeField(default=timezone.now)
    
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo} - {'Expirada' if self.status else 'Ativa'} - {self.aula}"
    
#Chamada (classe principal)

class Chamada(models.Model):
    id = models.AutoField(primary_key=True)
    horaEntrada = models.DateTimeField(null=True, blank=True)
    horaSaida = models.DateTimeField(null=True, blank=True)
    faltas = models.IntegerField(null=True, blank=True)

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    chave = models.ForeignKey(Chave, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.faltas is None:
            self.faltas = self.aula.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.aluno} - {self.aula} - {self.horaEntrada} - {self.horaSaida}"