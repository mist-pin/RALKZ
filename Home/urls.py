from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('faq/', views.faq),
    path('career/', views.career),
    path('career/apply/', views.apply_job),
    # path('service/', views.services),
    # path('about/', views.about),
    # path('orders/', views.orders),
]
