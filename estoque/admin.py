from django.contrib import admin
from .models import Categoria, Produto, Movimentacao

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Movimentacao)
