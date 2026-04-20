from django.db.models.signals import post_save #salva os negocio 
from django.dispatch import receiver #conecta o signal com funcao
from .models import Movimentacao

#decorator quando uma movimentacao for salva executa essa funcao
@receiver(post_save, sender=Movimentacao)

#instance a movimentacao criada | created True se foi criada agora 
def atualizar_estoque(sender, instance, created, **kwargs):
    
    if created:  # só quando criar (não quando editar)
        produto = instance.produto

        if instance.tipo == 'E': #entrada soma
            produto.quantidade += instance.quantidade

        elif instance.tipo == 'S': #saida subtrai
            produto.quantidade -= instance.quantidade

        produto.save()