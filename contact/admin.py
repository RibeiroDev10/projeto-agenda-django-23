# type: ignore
from django.contrib import admin
from contact.models import Contact
from contact.models import Category

# Register your models here.
@admin.register(Contact)  # Registrando meu model no site administrativo do Django
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'show')  # Definindo quais colunas irão aparecer no display
    ordering = ('-id',)  # Ordenando a coluna id por DECRESCENTE
    search_fields = 'id', 'first_name', 'last_name'  # Definindo quais campos podem ser buscados
    list_per_page = 10  # Definindo quantas listas por página
    list_max_show_all = 200  # Definindo o máximo de listas que podem ser mostradas
    list_editable = 'first_name', 'last_name', 'show'  # Quais campos podem ser editáveis
    list_display_links = 'id', 'phone'  # Campos que se tornam links <a>


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',
