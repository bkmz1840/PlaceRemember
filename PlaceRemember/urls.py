from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls'), name="login"),
    path('', include("social_django.urls"), name="social"),
    path('myPlaceRemember/', include("myPlaceRemember.urls"), name="home_page"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout")
]
