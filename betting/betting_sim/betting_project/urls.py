"""
URL configuration for betting_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import welcome, debug_info

urlpatterns = [
    # Debug welcome page at the root URL
    path('', welcome, name='welcome'),
    
    # Original URL patterns
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('simulation/', include('simulation.urls')),
    path('strategies/', include('strategies.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('debug-info/', debug_info, name='debug_info'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 