from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user = {
        "name": request.user.first_name + " " + request.user.last_name
    }
    return render(request, 'myPlaceRemember/index.html', user)
