from django import forms
from django.core.exceptions import ValidationError
from .models import RememberModel


class RememberModelForm(forms.Form):
    title = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'remember_body',
        'placeholder': 'Описание'}))

    title.widget.attrs.update({'class': 'form-control', 'id': 'remember_title',
                               'placeholder': 'Название'})
    location.widget.attrs.update({'class': 'form-control', 'id': 'remember_location',
                                  'placeholder': 'Поставьте точку на карте'})

    def clean_title(self):
        value = self.cleaned_data['title']
        if value.lower() == 'create':
            raise ValidationError('Название не может быть \'Create\'')
        if RememberModel.objects.filter(title__iexact=value).count():
            raise ValidationError('Воспоминание с таким названием уже существует')
        return value

    def get_slug_by_title(self, title):
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
        return title

    def save(self, profile):
        slug = self.get_slug_by_title(self.cleaned_data['title'])
        new_remember = RememberModel.objects.create(
            title=self.cleaned_data['title'],
            location=self.cleaned_data['location'],
            body=self.cleaned_data['body'],
            profile=profile,
            slug=slug
        )
        return new_remember
