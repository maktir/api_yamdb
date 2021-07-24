import django_filters
from .models import Title


class FilterSetTitle(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(field_name='name',
                                             lookup_expr='contains')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='exact')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='exact')

    class Meta:
        fields = ['name', 'genre', 'category', 'year']
        model = Title
