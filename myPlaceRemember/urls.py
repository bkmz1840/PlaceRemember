from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('create/', CreateRememberView.as_view(), name="create_remember"),
]
