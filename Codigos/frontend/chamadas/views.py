from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Professor, Chave, Disciplina, Diario, Aula, Aluno, Chamada
from .forms import AlunoForm, ProfessorForm

# Create your views here.

def registrar_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.save()

            codigo = form.cleaned_data['codigo']
            chave = Chave.objects.get(codigo=codigo)

            # Associar chave ao aluno
            chave.aluno = aluno
            chave.status = True
            chave.usadoEm = timezone.now()
            chave.save()

            return redirect("index")
    else:
        form = AlunoForm()

    return render(request, "paginas/formAluno.html", {"form": form})

class ProfessorCreate(CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'paginas/formProfessor.html'
    success_url = reverse_lazy("index")

class DisciplinaList(ListView):
    model = Disciplina
    template_name = 'paginas/listas/disciplina.html'

class DiarioList(ListView):
    model = Diario
    template_name = 'paginas/listas/diario.html'

class AulaList(ListView):
    model = Aula
    template_name = 'paginas/listas/aula.html'

class AlunoList(ListView):
    model = Aluno
    template_name = 'paginas/listas/aluno.html'

class ChamadaList(ListView):
    model = Chamada
    template_name = 'paginas/listas/chamada.html'