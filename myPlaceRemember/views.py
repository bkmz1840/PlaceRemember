from django.shortcuts import render, redirect, get_object_or_404
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
            return redirect('home')
        context = profile.get_name_and_avatar()
        context['form'] = bound_form
        return render(request, 'myPlaceRemember/create_remember.html',
                      context)


class UpdateRememberView(View):
    def get(self, request, slug):
        profile = get_profile_data_by_user(request.user)
        remember = RememberModel.objects.get(profile=profile, slug__iexact=slug)
        bound_form = RememberModelForm(remember)
        context = profile.get_name_and_avatar()
        context['remember'] = remember
        context['form'] = bound_form
        return render(request, "myPlaceRemember/update_remember.html", )


def remember_detail(request, slug):
    profile = get_profile_data_by_user(request.user)
    remember = RememberModel.objects.get(slug__iexact=slug)
    context = profile.get_name_and_avatar()
    context['remember'] = remember
    return render(request, 'myPlaceRemember/remember_detail.html', context)
