from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Funcionario
# Create your models here.


# base manager
class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# base model para estoque(produto, categoria, movimentacao)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #salva quando cria 
    updated_at = models.DateTimeField(auto_now=True) #atualiza sempre que salva
    is_deleted = models.BooleanField(default=False) # substitui delete(soft)

    objects = BaseManager() #so ativos
    all_objects = models.Manager() #tudo

# realiza o delete sem excluir do banco
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

# restaura o registro
    def restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted'])

    class Meta:
        abstract = True


# CLASSES PARA ESTOQUE



# herda tudo do basemodel
class Categoria(BaseModel):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    

class Produto(BaseModel):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)


    # relacionamento cada produto pertence a uma categoria 
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT, #nao deixa a categoria ser apagada se estiver ligadoa  produto
        related_name='produtos'
    )

    def __str__(self):
        return self.nome
    
class Movimentacao(BaseModel):
    #tipo de movimentacao
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saida'),
    )

    # produto ligado
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='movimentacoes'
    )

    # funcionario que fez a venda 
    funcionario = models.ForeignKey(
    Funcionario,
    on_delete=models.PROTECT,
    related_name='movimentacoes'
)

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True)
    
    def clean(self):
        if self.tipo == 'S' and self.quantidade > self.produto.quantidade:
            raise ValidationError("Estoque insuficiente")
    def save(self, *args, **kwargs):
        self.full_clean()  # garante validação
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} -  {self.tipo} - {self.quantidade}"