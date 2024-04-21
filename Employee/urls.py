from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_home),
    path('tl/', views.tl),
    path('pm/', views.pm),
    path('hpm/',views.hpm),
    path('tm/',views.tm),
    path('sm/',views.sm),
    path('md/', views.md),
    path('account/<str:emp_id>/', views.employee_account),
]
