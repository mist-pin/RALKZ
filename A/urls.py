
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('auth/', include('Auth.urls')),
    path('', include('Home.urls')),
    path('emp/', include('Employee.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Home.views._404'

