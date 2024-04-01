from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_home),
    path('<str:emp_id>/', views.employee)
]
