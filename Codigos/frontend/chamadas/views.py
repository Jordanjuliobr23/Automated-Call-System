from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Professor, Chave
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

    return render(request, "paginas/pages/formAluno.html", {"form": form})

class ProfessorCreate(CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'paginas/pages/formProfessor.html'
    success_url = reverse_lazy("index")