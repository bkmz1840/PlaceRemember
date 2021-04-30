from django.shortcuts import render, redirect


def index(request):
    if request.user.is_active:
        return redirect("myPlaceRemember/")
    return render(request, 'login/index.html')
