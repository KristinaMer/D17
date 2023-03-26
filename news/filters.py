from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Posts, Authors
from django import forms

class PostFilter(FilterSet):
    # date_create__gt = DateFilter(field_name='date_create', label='Start date', widget=forms.DateInput(
    #     attrs = {'type': 'date'}),lookup_expr = 'date__gte')
    # class Meta:
    #     model = Posts
    #     fields = {
    #         'header': ['icontains'],
    #         'authors': ['exact']
    #     }

    search_title = CharFilter(
        field_name = 'header',
        label = 'Название статьи',
        lookup_expr = 'icontains'
    )
    search_author = ModelChoiceFilter(
        empty_label = 'Все авторы',
        field_name = 'authors',
        label = 'Автор',
        queryset = Authors.objects.all()
    )
    post_date__gt = DateFilter(
        field_name = 'date_create',
        widget = forms.DateInput(attrs = {'type': 'date'}),
        label = 'Дата',
        lookup_expr = 'date__gte'
    )





