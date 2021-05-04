from django.db import models
from django.shortcuts import reverse
from login.models import Profile


def to_slug_from_title(title, username):
    dict_ru_to_us = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
                     'д': 'd', 'е': 'e', 'ё': 'e',
                     'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i',
                     'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                     'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
                     'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                     'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz',
                     'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                     'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V',
                     'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
                     'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I',
                     'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
                     'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
                     'У': 'U', 'Ф': 'F', 'Х': 'H',
                     'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH',
                     'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E',
                     'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_',
                     '~': '', '!': '', '@': '', '#': '',
                     '$': '', '%': '', '^': '', '&': '', '*': '',
                     '(': '', ')': '', '-': '', '=': '', '+': '',
                     ':': '', ';': '', '<': '', '>': '', '\'': '',
                     '"': '', '\\': '', '/': '', '№': '',
                     '[': '', ']': '', '{': '', '}': '', 'ґ': '',
                     'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
                     'Є': 'e', '—': ''}
    for key in dict_ru_to_us:
        title = title.replace(key, dict_ru_to_us[key])
    return username + "-" + title


class RememberModel(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    body = models.TextField(blank=True, db_index=True)
    slug = models.CharField(max_length=100, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('remember_detail', kwargs={'slug': self.slug})

    def get_absolute_update_url(self):
        return reverse('remember_update', kwargs={'slug': self.slug})

    def get_absolute_delete_url(self):
        return reverse('remember_delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = to_slug_from_title(self.title, self.profile.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
