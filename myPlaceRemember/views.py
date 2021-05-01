from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import Profile


@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    user_info = {
        "name": request.user.first_name + " " + request.user.last_name,
        "avatar": profile.avatar
    }
    return render(request, 'myPlaceRemember/index.html', user_info)
