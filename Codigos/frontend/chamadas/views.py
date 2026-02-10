from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, datetime
import hashlib

from .models import Professor, Chave, Disciplina, Diario, Aula, Aluno, Chamada, Horario, ProfessorDiario, AlunoDiario, DiarioHorario
from .forms import AlunoForm, ProfessorForm
from .funcoes import qr_image
from .suap import autenticar_suap, buscar_diarios

# 1. O professor clica no botão e gera a chave
def gerar_chave(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    chave = Chave.objects.create(
        aula=aula
    )

    return redirect('mostrar_qr', aula_id=aula_id, codigo=chave.codigo)


# 2. View que exibe o QR e inicia o cronômetro
def mostrar_qr(request, aula_id, codigo):
    aula = get_object_or_404(Aula, id=aula_id)
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
        "diario": aula.diario,
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

def professor_login(request):
    if request.method == "POST":
        form = ProfessorForm(request.POST)

        if form.is_valid():
            matricula = form.cleaned_data["matricula"]
            senha = form.cleaned_data["senha"]

            token = autenticar_suap(matricula, senha)

            if not token:
                form.add_error(None, "Matrícula ou senha inválidas.")
                return render(request, "paginas/formProfessor.html", {"form": form})

            diarios_api = buscar_diarios(token)

            if not diarios_api:
                form.add_error(None, "Erro ao buscar diários no SUAP.")
                return render(request, "paginas/formProfessor.html", {"form": form})
            
            hash_senha = hashlib.sha256(senha.encode()).hexdigest()

            for p1 in diarios_api[0]["professores"]:
                if p1["matricula"] == matricula:
                    nome = p1["nome"]
                    break

            if not nome:
                form.add_error(None, "Professor não encontrado nos diários do SUAP.")
                return render(request, "paginas/formProfessor.html", {"form": form})

            professor_logado, _ = Professor.objects.update_or_create(
                matricula=matricula,
                defaults={
                    "nome": nome,
                    "senha": hash_senha
                }
            )
            professor_logado.senha = hash_senha
            professor_logado.save(update_fields=["senha"])

            with transaction.atomic():
                for d in diarios_api:
                    componente_curricular = d["componente_curricular"].split(' - ')
                    disciplina, _ = Disciplina.objects.get_or_create(
                        id_suap = int(d["id"])+1,
                        sigla=componente_curricular[0],
                        nome=componente_curricular[1],
                        nivel=componente_curricular[2]
                    )
                    
                    diario, _ = Diario.objects.get_or_create(
                        id_suap = d["id"],
                        disciplina=disciplina,
                        defaults={
                        "local": d["locais_de_aula"][0]
                        }
                    )

                    for h in d["horarios"]:
                        horario, _ = Horario.objects.get_or_create(
                            dia=h["dia"],
                            horario=h["horario"]
                        )
                        DiarioHorario.objects.get_or_create(
                            diario=diario,
                            horario=horario
                        )

                    for p in d["professores"]:
                        if p["matricula"] == matricula:
                            professor = professor_logado
                        else:
                            professor, _ = Professor.objects.get_or_create(
                                matricula=p["matricula"],
                                defaults={"nome": p["nome"]}
                            )

                        ProfessorDiario.objects.get_or_create(
                            professor=professor,
                            diario=diario
                        ) 

                    for alu in d["participantes"]:
                        aluno, _ = Aluno.objects.get_or_create(
                            matricula = alu["matricula"],
                            defaults={
                                "nome": alu["nome"]
                            }
                        )    
                        AlunoDiario.objects.get_or_create(
                            aluno=aluno,
                            diario=diario
                        )

                    for a in d["aulas"]:
                        data_aula = datetime.strptime(a["data"], "%Y-%m-%d").date()
                        professor_aula = (
                            Professor.objects.filter(
                                nome=a["professor"], 
                                professordiario__diario=diario).first()
                        )
                        aula, _ = Aula.objects.get_or_create(
                            data=data_aula,
                            etapa=a["etapa"],
                            diario=diario,
                            defaults={
                                "quantidade": a["quantidade"],
                                "conteudo": a["conteudo"],
                                "professor": professor_aula
                            }
                        )

            return redirect("listar-diarios")

    else:
        form = ProfessorForm()

    return render(request, "paginas/formProfessor.html", {"form": form})


class DiarioList(ListView):
    model = Diario
    template_name = 'paginas/listas/diario.html'

def listar_aulas(request, diario_id):
    diario = get_object_or_404(Diario, id_suap=diario_id)

    aulas = Aula.objects.filter(diario=diario).order_by("data")

    return render(request, "paginas/listas/aula.html", {
        "diario": diario,
        "aulas": aulas
    })

def listar_alunos(request, diario_id):
    diario = get_object_or_404(Diario, id_suap=diario_id)

    alunos = AlunoDiario.objects.filter(diario=diario)

    return render(request, "paginas/listas/aluno.html", {
        "diario": diario,
        "alunos": alunos
    })

class AlunoList(ListView):
    model = Aluno
    template_name = 'paginas/listas/aluno.html'

class ChamadaList(ListView):
    model = Chamada
    template_name = 'paginas/listas/chamada.html'