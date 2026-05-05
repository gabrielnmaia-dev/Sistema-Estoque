from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from core.base_model import BaseModel

# Create your models here.


class Funcionario(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='funcionario'
    )
    cpf_validator = RegexValidator(r'^\d{11}$', 'CPF deve conter exatamente 11 números.')
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username