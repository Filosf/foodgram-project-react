from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status
from rest_framework.decorators import action

from api.serializers import (TagSerializer, UserMeSerializer, UserSerializer,
                             RecipeSerializer, RecipeCreatSerializer,
                             IngredientSerializer)
from api.permissions import IsAdmin
from recipes.models import Tag, User, Recipe, Ingredient


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViwsSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            "recipe_ingredients__ingredient", "tags"
        ).all()

    def get_serializer_class(self):
        if self.action == "create":
            return RecipeCreatSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "username"
    filter_backends = (filters.SearchFilter, )
    search_fields = ("username",)
    http_method_names = ["get", "post", "patch", "delete"]

    @action(detail=False, methods=["get", "patch"],
            permission_classes=[IsAuthenticated],
            serializer_class=UserMeSerializer,
            pagination_class=None)
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
