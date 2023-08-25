from rest_framework import serializers

from recipes.models import Tag, User, Recipe, RecipeIngredients, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Mets:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredients
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source="recipe_ingredients"
    )

    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeCreatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("name", "cooking_time", "text", "tags", "ingredients")


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "role")
        read_only_fields = ("role",)
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "role")
        model = User
