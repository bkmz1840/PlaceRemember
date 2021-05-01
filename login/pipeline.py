from .models import Profile
from django.shortcuts import get_object_or_404


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    if backend.name == 'vk-oauth2':
        url = response.get('photo', '')
    if url:
        try:
            profile = Profile.objects.get(user=user)
            profile.avatar = url
        except:
            profile = Profile.objects.create(user=user, avatar=url)
        finally:
            profile.save()
