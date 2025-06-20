import django_filters
from .models import News

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category__id')
    tags = django_filters.NumberFilter(field_name='tags__id')

    class Meta:
        model = News
        fields = ['title', 'category', 'tags']
