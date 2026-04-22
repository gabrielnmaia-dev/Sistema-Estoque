from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioEditForm
# Create your views here.
#>>>>>>>>>>>>>>>>>>>> views func <<<<<<<<<<<<
class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'usuarios/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10

class FuncionarioCreateView(CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'usuarios/funcionarios_form.html'
    success_url = reverse_lazy('funcionario-list')

class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    form_class = FuncionarioEditForm
    template_name = 'usuarios/funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')

def funcionario_toggle_active(request, pk):
    #view pra ativar e desativar func
    funcionario = get_object_or_404(Funcionario, pk=pk)
    #inverte o status de ativo/desativo do func
    funcionario.user.is_active = not funcionario.user.is_active
    funcionario.user.save()

    return redirect('funcionario-list')
