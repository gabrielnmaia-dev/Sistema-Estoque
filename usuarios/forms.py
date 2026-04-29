from django import forms
from django.contrib.auth.models import User
from .models import Funcionario

#>>>>>>>>>>>>>>>>>>>> form pra criar funcionario <<<<<<<<<<<<<<<<<<<<<<<
class FuncionarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    #esse widge pra carregar o <input type='password'>

    class Meta:
        model = Funcionario
        fields = ['cpf', 'telefone']
    
    def save(self, commit=True):
        #cria um user e depois um funcionario

        user = User.objects.crete_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )

        funcionario = super().save(commit=False)
        funcionario.user = user
        #aqui vai salvar o funcionario
        if commit:
            funcionario.save()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Form editar func <<<<<<<<<<<<<<<<<<<

class FuncionarioEditForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Funcionario
        fields = ['cpf', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #pra editar func existente
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        #att func e o user
        funcionario = super().save(commit=False)

        funcionario.user.username = self.cleaned_data['username']
        funcionario.user.email = self.cleaned_data['email']
        funcionario.user.save()
        
        # Salva o Funcionario
        if commit:
            funcionario.save()
        
        return funcionario 
