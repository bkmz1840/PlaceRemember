from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from login.models import Profile
from .forms import RememberModelForm
from .models import RememberModel


def get_profile_data_by_user(user):
    try:
        return Profile.objects.get(user=user)
    except:
        raise ValueError("Такой пользователь не найден")


@login_required
def index(request):
    profile = get_profile_data_by_user(request.user)
    remembers = RememberModel.objects.all().filter(profile=profile)
    context = profile.get_name_and_avatar()
    context['remembers'] = remembers
    return render(request, 'myPlaceRemember/index.html',
                  context)


class CreateRememberView(View):
    def get(self, request):
        context = get_profile_data_by_user(request.user).get_name_and_avatar()
        context['form'] = RememberModelForm()
        return render(request, 'myPlaceRemember/create_remember.html',
                      context)

    def post(self, request):
        bound_form = RememberModelForm(request.POST)
        profile = get_profile_data_by_user(request.user)
        if bound_form.is_valid():
            new_remember = bound_form.save(profile)
            new_remember.save()
            return redirect('myPlaceRemember/')
        context = profile.get_name_and_avatar()
        context['form'] = bound_form
        return render(request, 'myPlaceRemember/create_remember.html',
                      context)
