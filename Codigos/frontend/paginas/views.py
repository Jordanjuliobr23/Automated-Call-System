from django.views.generic import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name= 'paginas/pages/index.html'

class ProfessorView(TemplateView):
    template_name= 'paginas/pages/professor.html'