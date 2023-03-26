from django import forms
from django.core.exceptions import ValidationError
from .models import Posts, Authors

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            'authors',
            'header',
            'body',
            'name_category'
        ]

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get('header')
        body = cleaned_data.get('body')
        if body is not None and body == header:
            raise ValidationError({
                'body': 'Текст статьи не должен быть идентичен заголовоку'
            })
        return cleaned_data












