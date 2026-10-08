import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name="author__username",
        lookup_expr="iexact"
    )

    category = django_filters.CharFilter(
        field_name="category__title",
        lookup_expr="iexact"
    )

    class Meta:
        model = Post
        fields = ["author", "category"]