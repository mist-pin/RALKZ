
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Auth.urls')),
    path('', include('Home.urls')),
    path('emp/', include('Employee.urls')),
]


handler404 = 'Home.views._404'

