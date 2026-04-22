from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
# apenas para rodar migrate

#>>>>>>>>>>>>>>>>>>>>>>>>>Produto link<<<<<<<<<<<<<<<<<<
#mostra todos os produtos
path('produtos/', views.ProdutoListView.as_view(), name='produto-list'),
path('produtos/criar/', views.ProdutoCreateView.as_view(), name='produto-create'),
#editar um produto que JÁ existe, o resto é auto explicativo
path('produtos/<int:pk>/editar/', views.ProdutoUpdateView.as_view(), name='produto-updated'),
path('produtos/<int:pk>/deletar', views.produto_delete, name='produto-delete'),

#>>>>>>>>>>>>>>>>>>>>>>>>>> Categoria links <<<<<<<<<<<<<<<<<<<<<<
path('categorias/', views.CategoriaListView.as_view(),name='produto-list'),
path('categorias/criar/', views.CategoriaCreateView.as_view(), name='categoria-create'),
path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
path('produtos/<int:pk>/deletar/', views.categoria_delete, name='categoria-delete'),

]