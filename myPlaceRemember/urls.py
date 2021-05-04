from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('create/', CreateRememberView.as_view(), name="create_remember"),
    path('<str:slug>/', remember_detail, name="remember_detail"),
    path('<str:slug>/edit/', UpdateRememberView.as_view(), name="remember_update"),
    path('<str:slug>/del', remember_delete, name="remember_delete"),
]
