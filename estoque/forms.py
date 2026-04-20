from django import forms #sistema de formularios
from .models import Movimentacao  

class MovimentacaoForm(forms.ModelForm): #cira um form automatico baseado no model 
    class Meta:
        model = Movimentacao #model
        fields = ['produto', 'tipo', 'quantidade', 'observacao'] #campos do form