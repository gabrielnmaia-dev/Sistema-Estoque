from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from estoque.models import Produto, Movimentacao
from estoque.forms import VendaForm
from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioEditForm


# MIXIN — Restringe acesso apenas a Gerentes (ou superusuário)
# Herda LoginRequiredMixin (exige login) + UserPassesTestMixin (exige o teste)
class GerenteRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        # Passa se for do grupo Gerente OU se for superusuário/staff
        return (
            self.request.user.groups.filter(name='Gerente').exists()
            or self.request.user.is_staff
        )

    def handle_no_permission(self):
        # Se está logado mas não é gerente, manda para a dash do vendedor
        # Se não está logado, o LoginRequiredMixin redireciona para o login
        if self.request.user.is_authenticated:
            return redirect('vendedor-dashboard')
        return super().handle_no_permission()


# LOGIN / LOGOUT
# Usamos as CBVs nativas do Django — só customizamos o redirecionamento
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def form_valid(self, form):
        # Faz o login (salva na sessão) sem redirecionar ainda
        from django.contrib.auth import login
        login(self.request, form.get_user())
        
        user = self.request.user
        if user.groups.filter(name='Gerente').exists() or user.is_staff:
            return redirect('gerente-dashboard')
        return redirect('vendedor-dashboard')

class CustomLogoutView(LogoutView):
    # Após logout, redireciona para o login
    next_page = reverse_lazy('login')


# FUNCIONÁRIOS — apenas Gerente acessa
class FuncionarioListView(GerenteRequiredMixin, ListView):
    model = Funcionario
    template_name = 'usuarios/funcionario_list.html'
    context_object_name = 'funcionarios'
    paginate_by = 10

    def get_queryset(self):
        # select_related evita N+1 queries ao acessar funcionario.user no template
        qs = Funcionario.objects.select_related('user').order_by('user__username')

        # Filtro de busca por nome de usuário via ?q=
        busca = self.request.GET.get('q', '').strip()
        if busca:
            qs = qs.filter(user__username__icontains=busca)

        return qs


class FuncionarioCreateView(GerenteRequiredMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'usuarios/funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Passamos título e label do botão para reaproveitar o mesmo template no update
        ctx['titulo'] = 'Cadastrar Vendedor'
        ctx['btn_label'] = 'Cadastrar'
        return ctx


class FuncionarioUpdateView(GerenteRequiredMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioEditForm
    template_name = 'usuarios/funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Vendedor'
        ctx['btn_label'] = 'Salvar alterações'
        return ctx


def funcionario_toggle_active(request, pk):
    """Ativa ou desativa o login de um funcionário — apenas Gerente."""

    # Verificação manual já que é FBV
    if not (request.user.is_staff or request.user.groups.filter(name='Gerente').exists()):
        return redirect('vendedor-dashboard')

    funcionario = get_object_or_404(Funcionario, pk=pk)
    # Inverte o is_active do User vinculado
    funcionario.user.is_active = not funcionario.user.is_active
    funcionario.user.save()

    return redirect('funcionario-list')


# DASHBOARD DO GERENTE
# Visão geral do sistema: estoque, movimentações, alertas
class GerenteDashboardView(GerenteRequiredMixin, TemplateView):
    template_name = 'usuarios/gerente_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        hoje = timezone.now().date()

        # Totais gerais
        ctx['total_produtos'] = Produto.objects.count()
        ctx['funcionarios_ativos'] = Funcionario.objects.filter(
            user__is_active=True
        ).count()

        # Produtos com estoque abaixo de 5 — alerta visual no template
        ctx['estoque_baixo'] = Produto.objects.filter(quantidade__lt=5)

        # Movimentações recentes de todos os funcionários
        # select_related evita queries extras ao acessar produto e funcionario.user
        ctx['movimentacoes_recentes'] = Movimentacao.objects.select_related(
            'produto', 'funcionario__user'
        ).order_by('-data')[:10]

        # Contagem de entradas e saídas do dia atual
        ctx['saidas_hoje'] = Movimentacao.objects.filter(
            tipo='S', data__date=hoje
        ).count()
        ctx['entradas_hoje'] = Movimentacao.objects.filter(
            tipo='E', data__date=hoje
        ).count()

        return ctx


# DASHBOARD DO VENDEDOR
# Mostra apenas os dados do próprio vendedor logado
class VendedorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/vendedor_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        # Se for gerente ou staff, redireciona para a dash correta
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.groups.filter(name='Gerente').exists():
                return redirect('gerente-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        hoje = timezone.now().date()

        # Tenta pegar o funcionario vinculado ao usuário logado
        # Superusuário pode não ter Funcionario — o try evita crash
        try:
            funcionario = self.request.user.funcionario

            # Movimentações do próprio vendedor, as 10 mais recentes
            ctx['movimentacoes'] = Movimentacao.objects.filter(
                funcionario=funcionario
            ).select_related('produto').order_by('-data')[:10]

            # Total de saídas que ele fez hoje
            ctx['saidas_hoje'] = Movimentacao.objects.filter(
                funcionario=funcionario,
                tipo='S',
                data__date=hoje
            ).count()

        except Funcionario.DoesNotExist:
            ctx['movimentacoes'] = []
            ctx['saidas_hoje'] = 0

        # Produtos disponíveis em estoque (qualquer vendedor pode ver)
        ctx['produtos'] = Produto.objects.filter(
            quantidade__gt=0
        ).order_by('nome')
        ctx['venda_form'] = VendaForm()

        return ctx

class VendaCreateView(LoginRequiredMixin, CreateView):
    model = Movimentacao
    form_class = VendaForm
    template_name = 'usuarios/venda_form.html'
    success_url = reverse_lazy('vendedor-dashboard')

    def dispatch(self, request, *args, **kwargs):
        #gerente n entra nessa view
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.groups.filter(name='Gerente').exists():
                return redirect('gerente-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        funcionario = getattr(self.request.user, 'funcionario', None)
        #aqui verifica se é None o usuário
        if not funcionario:
            form.add_error(None, 'Seu usuário não possui perfil de funcionário')
            return self.form_invalid(form)
        
        movimentacao = form.save(commit=False) #cria o objeto
        movimentacao.tipo = 'S'                #faz o tipo de saída
        movimentacao.funcionario = funcionario #vincula o processo ao vendedor logado

        movimentacao.full_clean()
        movimentacao.save() #aqui é onde o produto é descontado do estoque
        return redirect(self.success_url)