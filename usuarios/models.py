from django.db import models
from django.conf import settings

# Create your models here.


class Funcionario(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='funcionario'
    )
    
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username