from django.contrib import admin
from .models import Professor, Diario, Disciplina

# Register your models here.

admin.site.register(Professor)
admin.site.register(Diario)
admin.site.register(Disciplina)