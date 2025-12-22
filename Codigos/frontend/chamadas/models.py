from django.db import models
from django.utils import timezone
import secrets

# Bloco Superior até Chamada

class Professor(models.Model):
    matricula = models.CharField(max_length=14, verbose_name="Matrícula", unique=True, primary_key=True)
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nome} | {self.matricula}"
    
class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=20)
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.sigla} | {self.nome}"

class Diario(models.Model):
    id = models.AutoField(primary_key=True)

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, blank=True, null=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.disciplina} | {self.professor}"
    
class Horario(models.Model):
    DIA = (('Domingo','Domingo'),('Segunda','Segunda'),('Terça','Terça'),('Quarta','Quarta'),('Quinta','Quinta'),('Sexta','Sexta'),('Sábado','Sábado'))

    id = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=7, choices=DIA)
    horaInicio = models.TimeField()
    horaFim = models.TimeField()

    def __str__(self):
        return f"{self.dia} | {self.horaInicio.strftime('%H:%M')} | {self.horaFim.strftime('%H:%M')}"
    
class Aula(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    etapa = models.IntegerField()
    quantidade = models.IntegerField()
    conteudo = models.TextField(blank=True, null=True)
    
    diario = models.ForeignKey(Diario, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.quantidade} | {self.data.strftime('%d/%m/%Y')} | {self.conteudo}"
    

# Bloco inferior até chamada
    
class Chave(models.Model):
    codigo = models.CharField(max_length=64, primary_key=True, unique=True, verbose_name="Código",default=secrets.token_urlsafe)
    status = models.BooleanField(default=False)
    criadoEm = models.DateTimeField(default=timezone.now)
    
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo} | {'Expirada' if self.status else 'Ativa'} | {self.aula}"
    
class Aluno(models.Model):
    matricula = models.CharField(max_length=14, primary_key=True, unique=True, verbose_name="Matrícula")
    nome = models.CharField(max_length=150)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nome} | {self.matricula}"

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
        return f"{self.aluno} | {self.aula} | {self.horaEntrada} | {self.horaSaida} | {self.presencas}"