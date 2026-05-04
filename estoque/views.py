from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm
from usuarios.views import GerenteRequiredMixin

# Create your views here.

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Views do produto<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class ProdutoListView(GerenteRequiredMixin, ListView): #view pra mostrar os produtos e junto com as páginas
    model = Produto
    template_name = 'estoque/produto-list.html' #onde achar o template
    context_object_name = 'produtos'
    paginate_by = 10 #paginação
    ordering = ['nome']

class ProdutoCreateView(GerenteRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'estoque/produto_form.html'
    success_url = reverse_lazy('produto-list') #pra ir depois de ter dado certo a criação do produto

class ProdutoUpdateView(GerenteRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'estoque/produto_form.html'
    success_url = reverse_lazy('produto-list')

def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    #vaio marcar como deletado aqui
    produto.delete()
    return redirect('produto-list')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Views da categoria<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class CategoriaListView(GerenteRequiredMixin, ListView):
    model = Categoria
    template_name = 'estoque/categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10

class CategoriaCreateView(GerenteRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'estoque/categoria_form.html'
    success_url = reverse_lazy('categoria-list')

class CategoriaUpdateView(GerenteRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'estoque/categoria_form.html'
    success_url = reverse_lazy('categoria-list')

def categoria_delete(request, pk): #bicho isso aqui é uma view pro softdelete da categoria
    categoria = get_object_or_404(Categoria,pk=pk)
    categoria.delete()
    return redirect('categoria-list')
