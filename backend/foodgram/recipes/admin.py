from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingList, Tag, User, Subscription)


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'count_favorites',)
    search_fields = ('author__username', 'author__email',
                     'author__first_name', 'author__last_name',)
    list_filter = ('author', 'name', 'tags',)
    ordering = ('name',)
    empty_value_display = '-пусто-'
    inlines = [TagInline, IngredientInline]

    def count_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    count_favorites.short_description = 'Количество избранных'


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredients)
admin.site.register(Favorite)
admin.site.register(ShoppingList)
admin.site.register(User)
admin.site.register(Subscription)
