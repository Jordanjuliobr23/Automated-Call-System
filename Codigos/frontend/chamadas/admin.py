from django.contrib import admin
from .models import Professor, Disciplina, Diario, Horario, Aula, Aluno, Chave, Chamada 

# Register your models here.

admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Diario)
admin.site.register(Horario)
admin.site.register(Aula)
admin.site.register(Aluno)
admin.site.register(Chave)
admin.site.register(Chamada)