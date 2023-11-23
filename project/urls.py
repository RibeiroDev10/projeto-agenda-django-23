from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Incluindo as URLs do meu APP -> contact.
    # Basicamente estou falando: Para a URL raiz do meu projeto
    # Inclua depois, as URLs do meu app contact.
    path('', include('contact.urls')),
    path('admin/', admin.site.urls),
]

               # Primeiro, o caminho das MEDIAS STATICS, depois a pasta raiz das MEDIAS
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)