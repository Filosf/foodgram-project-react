from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action

from api.serializers import (TagSerializer, UserSerializer, RecipeSerializer,
                             SubscriptionSerializer, IngredientSerializer,
                             RecipeGetSerializer, RecipeFollowSerializer)
from api.permissions import IsAuthorOrReadOnly
from recipes.models import (Tag, User, Recipe, Ingredient, Favorite,
                            ShoppingList, Subscription)
from api.utils import (add_favorite_shoppinglist, remove_favorite_shoppinglist)
from api.filters import RecipeFilter
from api.paginations import CastomPagination


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViwsSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CastomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        is_favorited = self.request.query_params.get("is_favorited")
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart")
        if is_favorited is not None and int(is_favorited) == 1:
            queryset = queryset.filter(favorite_recipe__user=self.request.user)
        elif is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            queryset = queryset.filter(shopping_list__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeGetSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action != "create":
            return (IsAuthorOrReadOnly(),)
        return super().get_permissions()

    @action(detail=True, methods=["POST", "DELETE"],)
    def favorite(self, request, pk):
        if self.request.method == "POST":
            return add_favorite_shoppinglist(request, pk, Favorite,
                                             RecipeFollowSerializer)
        return remove_favorite_shoppinglist(request, pk, Favorite)

    @action(detail=True, methods=["POST", "DELETE"],)
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            return add_favorite_shoppinglist(request, pk, ShoppingList,
                                             RecipeFollowSerializer)
        return remove_favorite_shoppinglist(request, pk, ShoppingList)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CastomPagination

    @action(
        detail=True, permission_classes=[IsAuthenticated],
        methods=["post", "delete"]
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get("id"))

        if request.method == "POST":
            serializer = SubscriptionSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=user, author=author)
            return Response(author.id, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            get_object_or_404(Subscription, user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=["GET"])
    def subscriptions(self, request):
        queryset = User.objects.filter(follower__user=request.user)
        serializer = SubscriptionSerializer(
            self.paginate_queryset(queryset),
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
