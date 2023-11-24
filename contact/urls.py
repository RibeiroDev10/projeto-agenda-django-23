from django.urls import path
from contact import views

# Definindo um namespace para as URLS desse APP
app_name = 'contact'

urlpatterns = [
    path('<int:contact_id>/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('', views.index, name='index'),
]
