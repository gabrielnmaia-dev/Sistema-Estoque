from django import forms
from django.contrib.auth.models import User
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Funcionario
        fields = ['cpf', 'telefone']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )

        funcionario = super().save(commit=False)
        funcionario.user = user
        if commit:
            funcionario.save()
        return funcionario


class FuncionarioEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Funcionario
        fields = ['cpf', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        if funcionario.user:
            funcionario.user.username = self.cleaned_data['username']
            funcionario.user.email = self.cleaned_data['email']
            funcionario.user.save()
        if commit:
            funcionario.save()
        return funcionario