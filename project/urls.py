from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Incluindo as URLs do meu APP -> contact.
    # Basicamente estou falando: Para a URL raiz do meu projeto
    # Inclua depois, as URLs do meu app contact.
    path('', include('contact.urls')),
    path('admin/', admin.site.urls),
]
