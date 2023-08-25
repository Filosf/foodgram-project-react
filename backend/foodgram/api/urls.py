from django.urls import include, path
from rest_framework import routers

from api.views import TagViewSet, UserViewSet, RecipeViewSet, IngredientViwsSet
from api.utils import ShoppingListDownloadView


app_name = 'api'

router = routers.DefaultRouter()
router.register("tags", TagViewSet)
router.register("users", UserViewSet)
router.register("recipes", RecipeViewSet)
router.register("ingredients", IngredientViwsSet, basename="ingredients")

urlpatterns = [
    path("recipes/download_shopping_cart/", ShoppingListDownloadView.as_view(),
         name="download_shopping_cart"),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
