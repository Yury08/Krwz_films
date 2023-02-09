from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='user')),
    path('', include('films.urls', namespace='films')),
]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)