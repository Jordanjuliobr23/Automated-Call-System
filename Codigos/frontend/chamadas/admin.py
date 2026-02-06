from django.contrib import admin
from .models import Professor, Disciplina, Diario, Horario, Aula, Aluno, Chave, Chamada, ProfessorDiario, AlunoDiario

# Register your models here.

admin.site.register(Disciplina)
admin.site.register(Horario)
admin.site.register(Aula)
admin.site.register(Chave)
admin.site.register(Chamada)

class ProfessorDiarioInline(admin.TabularInline):
    model = ProfessorDiario
    extra = 1
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("matricula", "nome")
    inlines = [ProfessorDiarioInline]

class AlunoDiarioInline(admin.TabularInline):
    model = AlunoDiario
    extra = 1
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "nome")
    inlines = [AlunoDiarioInline]

@admin.register(Diario)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("id", "disciplina")
