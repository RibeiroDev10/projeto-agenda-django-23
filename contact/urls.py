from django.urls import path
from contact import views

# Definindo um namespace para as URLS desse APP
app_name = 'contact'

urlpatterns = [
    path('', views.index, name='index'),
]
