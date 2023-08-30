from django.contrib.auth.models import AnonymousUser
import django_filters

from recipes.models import User, Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = django_filters.NumberFilter(method="is_favorited_filter")
    is_in_shopping_cart = django_filters.NumberFilter(
        method="is_in_shopping_cart_filter")

    class Meta:
        model = Recipe
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")

    def is_favorited_filter(self, queryset, name, value):
        request_user = self.request.user
        if not isinstance(request_user, AnonymousUser):
            is_favorited = self.request.query_params.get("is_favorited")
            if is_favorited is not None and int(is_favorited) == 1:
                queryset = queryset.filter(
                    favorite_recipe__user=self.request.user
                )
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart")
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            queryset = queryset.filter(shopping_list__user=self.request.user)
        return queryset
