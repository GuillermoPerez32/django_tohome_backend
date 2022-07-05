from django.contrib import admin
from django_restful_admin import admin as rest_admin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()

# Pettern Example
#router.register(r'url', views_dir.View, basename='model')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/', rest_admin.site.urls),
    path('',include(router.urls)),
    path('api/', include('ecommerce.urls')),
    path('api/', include('directorio.urls')),
    path('auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
