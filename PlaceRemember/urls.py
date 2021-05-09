from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url='favicon.ico', permanent=True)),
    path('', include('login.urls'), name="login"),
    path('', include("social_django.urls"), name="social"),
    path('myPlaceRemember/', include("myPlaceRemember.urls"), name="home_page"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout")
]
