from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]


# apenas para rodar migrate