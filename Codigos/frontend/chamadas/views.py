from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Professor, Chave, Disciplina, Diario, Aula, Aluno, Chamada
from .forms import AlunoForm, ProfessorForm
import io, qrcode
from datetime import timedelta
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .funcoes import qr_image


# 1. O professor clica no botão e gera a chave
def gerar_chave(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    chave = Chave.objects.create(
        aula=aula
    )

    return redirect('mostrar_qr', codigo=chave.codigo)


# 2. View que exibe o QR e inicia o cronômetro
def mostrar_qr(request, codigo):
    chave = get_object_or_404(Chave, codigo=codigo)

    agora = timezone.now()
    expira_em = chave.criadoEm + timedelta(seconds=90)
    segundos_restantes = (expira_em - agora).total_seconds()

    if segundos_restantes < 0:
        segundos_restantes = 0

    qr_code = qr_image(codigo)

    return render(request, "paginas/mostrar_qr.html", {
        "chave": chave,
        "segundos_restantes": int(segundos_restantes),
        "qr_code": qr_code,
    })


# 3. JS chama esta view quando o tempo termina
@csrf_exempt
def expirar_chave(request, codigo):
    if request.method == "POST":
        try:
            chave = Chave.objects.get(codigo=codigo)
            chave.status = True
            chave.save()
        except Chave.DoesNotExist:
            pass

    return HttpResponse("ok")


# 4. O aluno acessa a URL do QR e registra presença
def registrar_aluno(request, codigo):
    chave = get_object_or_404(Chave, codigo=codigo)

    if request.method == "POST":
        data = request.POST.copy()
        data["codigo"] = chave.codigo  # força o valor correto no backend

        form = AlunoForm(data)

        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.chave = chave
            aluno.save()

            # redireciona à página inicial
            return redirect('index')
    else:
        # Preenche o campo código, mas impede edição
        form = AlunoForm(initial={"codigo": chave.codigo})

    return render(request, "paginas/formAluno.html", {
        "form": form,
        "codigo": chave.codigo,
    })

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