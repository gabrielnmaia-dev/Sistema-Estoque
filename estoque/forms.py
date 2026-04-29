from django import forms #sistema de formularios
from .models import Produto, Movimentacao, Categoria

class ProdutoForm(forms.ModelForm): #cira um form automatico baseado no model 
    class Meta:
        model = Produto #model
        fields = ['nome', 'preco', 'descricao', 'quantidade', 'categoria'] #campos do form
        widgets={
            'nome': forms.TextInput(),
            'descricao': forms.TextInput(),
            'preco': forms.NumberInput(),
            'quantidade':forms.NumberInput(),   #pra cirar os <input type = 'number' ou 'text'>
            'categoria': forms.Select(),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']  #colocar a caixa de texto
        widgets = {
            'nome': forms.TextInput()
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'tipo', 'quantidade', 'observacao']