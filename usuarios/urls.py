from django.urls import path
from . import views

# Lista de todas as rotas do app usuarios
urlpatterns = [
    # # LISTAR todos os funcionários
    # path('funcionarios/', views.FuncionarioListView.as_view(), name='funcionario-list'),
    
    # # CRIAR novo funcionário
    # path('funcionarios/criar/', views.FuncionarioCreateView.as_view(), name='funcionario-create'),
    
    # # EDITAR funcionário
    # path('funcionarios/<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='funcionario-update'),
    
    # # ATIVAR/DESATIVAR funcionário
    # path('funcionarios/<int:pk>/toggle/', views.funcionario_toggle_active, name='funcionario-toggle'),

    # path('login/', views.CustomLoginView.as_view(), name='login'),


    # path('dashboard/', views.VendedorDashboardView.as_view(), name='vendedor_dashboard'),

    # path('dashboard/gerente/', views.GerenteDashboardView.as_view(), name='gerente-dashboard'),

    path('', views.CustomLoginView.as_view(), name='login'),  # raiz aponta pro login
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('funcionarios/', views.FuncionarioListView.as_view(), name='funcionario-list'),
    path('funcionarios/cadastrar/', views.FuncionarioCreateView.as_view(), name='funcionario-create'),
    path('funcionarios/<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='funcionario-update'),
    path('funcionarios/<int:pk>/toggle/', views.funcionario_toggle_active, name='funcionario-toggle'),

    path('dashboard/', views.VendedorDashboardView.as_view(), name='vendedor-dashboard'),
    path('dashboard/gerente/', views.GerenteDashboardView.as_view(), name='gerente-dashboard'),
]