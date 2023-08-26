from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingList, Tag, User, Subscription)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name', 'color', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    ordering = ('name',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name',)
    ordering = ('id',)
    empty_value_display = '-пусто-'


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'


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


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class ShoppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingAdmin)
admin.site.register(User)
admin.site.register(Subscription, SubscribeAdmin)
