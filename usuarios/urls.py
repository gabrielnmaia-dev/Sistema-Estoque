from django.urls import path
from . import views

# Lista de todas as rotas do app usuarios
urlpatterns = [
    # LISTAR todos os funcionários
    path('funcionarios/', views.FuncionarioListView.as_view(), name='funcionario-list'),
    
    # CRIAR novo funcionário
    path('funcionarios/criar/', views.FuncionarioCreateView.as_view(), name='funcionario-create'),
    
    # EDITAR funcionário
    path('funcionarios/<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='funcionario-update'),
    
    # ATIVAR/DESATIVAR funcionário
    path('funcionarios/<int:pk>/toggle/', views.funcionario_toggle_active, name='funcionario-toggle'),
]