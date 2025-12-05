from django import forms
from .models import Aluno, Chave, Professor

class AlunoForm(forms.ModelForm):
    codigo = forms.CharField(label="Código de Autenticação")

    class Meta:
        model = Aluno
        fields = ["matricula", "senha", "codigo"]
        widgets = {
            "senha": forms.PasswordInput()
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")

        try:
            chave = Chave.objects.get(codigo=codigo)
        except Chave.DoesNotExist:
            raise forms.ValidationError("Código inválido.")

        if chave.status:
            raise forms.ValidationError("Este código já foi usado.")

        return codigo

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ["matricula", "senha"]
        widgets = {
            "senha": forms.PasswordInput()
        }