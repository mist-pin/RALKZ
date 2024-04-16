from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_home),
    path('tl/', views.tl),
    path('pm/', views.pm),
    path('md/', views.md),
    path('account/', views.employee_account),
]
