from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_home),
    path('pm/<str:emp_id>', views.pm),
    path('md/', views.md),
    path('acc/<str:emp_id>/', views.employee_account),
]
