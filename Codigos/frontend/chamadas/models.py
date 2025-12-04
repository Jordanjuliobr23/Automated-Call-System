from django.db import models
from django.utils import timezone

# Bloco Superior até Chamada

class Professor(models.Model):
    matricula = models.CharField(max_length=14, verbose_name="Matrícula", unique=True, primary_key=True)
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nome} | {self.matricula}"
    
class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=20)
    curso = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome} | {self.sigla}"

class Diario(models.Model):
    TURNOS = (('M', 'Matutino'),('V', 'Vespertino'),('N', 'Noturno'))

    id = models.AutoField(primary_key=True)
    turno = models.CharField(max_length=30, choices=TURNOS)

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, blank=True, null=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.professor} | {self.turno} | {self.disciplina}"
    
class Horario(models.Model):
    id = models.AutoField(primary_key=True)
    horaInicio = models.TimeField()
    horaFim = models.TimeField()
    tolerancia = models.TimeField()

    def __str__(self):
        return f"{self.horaInicio.strftime('%H:%M')} | {self.horaFim.strftime('%H:%M')}"
    
class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    numAula = models.IntegerField()
    conteudo = models.TextField(blank=True, null=True)
    
    diario = models.ForeignKey(Diario, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.numAula} | {self.diario.disciplina.nome} | {self.data.strftime('%d/%m/%Y')}"
    

# Bloco inferior até chamada

class Aluno(models.Model):
    matricula = models.CharField(max_length=14, primary_key=True, unique=True, verbose_name="Matrícula")
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome} | {self.matricula}"
    
class Chave(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True, unique=True, verbose_name="Código")
    status = models.BooleanField(default=False)
    criadoEm = models.DateTimeField(default=timezone.now)
    usadoEm = models.DateTimeField(null=True, blank=True)
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE,  null=True, blank=True)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} | {'Usada' if self.status else 'Ativa'} | {self.aluno}"


#Chamada (classe principal)

class Chamada(models.Model):
    id = models.AutoField(primary_key=True)
    horaEntrada = models.DateTimeField(null=True, blank=True)
    horaSaida = models.DateTimeField(null=True, blank=True)
    presencas = models.IntegerField(default=0)
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.SET_NULL, null=True, blank=True)
    chave = models.ForeignKey(Chave, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.aluno} | {self.aula} | {self.horaEntrada} | {self.horaSaida} | {self.presencas}"