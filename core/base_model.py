from django.db import models

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

