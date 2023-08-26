import io

from django.db.models import Sum
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe, RecipeIngredients


class ShoppingListDownloadView(APIView):
    def get(self, request):
        user = request.user
        shopping_list = RecipeIngredients.objects.filter(
            recipe__shopping_list__user=user).values(
            "ingredient__name",
            "ingredient__measurement_unit"
        ).annotate(
            amount=Sum("amount")
        ).order_by()
        font = "Tantular"
        pdfmetrics.registerFont(
            TTFont("Tantular",
                   "./Tantular.ttf",
                   "UTF-8")
        )
        buffer = io.BytesIO()
        pdf_file = canvas.Canvas(buffer)
        pdf_file.setFont(font, settings.SHOPPING_LIST_SETFONTS)
        pdf_file.drawString(
            settings.SHOPPING_LIST_TITLE_X,
            settings.SHOPPING_LIST_TITLE_Y,
            "Список покупок:"
        )
        pdf_file.setFont(font, settings.SHOPPING_LIST_SETFONT)
        from_bottom = settings.SHOPPING_LIST_BOTTOM_Y
        for number, ingredient in enumerate(shopping_list, start=1):
            pdf_file.drawString(
                settings.SHOPPING_LIST_ITEM_X,
                from_bottom,
                (f'{number}.  {ingredient["ingredient__name"]} - '
                 f'{ingredient["amount"]} '
                 f'{ingredient["ingredient__measurement_unit"]}')
            )
            from_bottom -= settings.SHOPPING_LIST_ITEM_HEIGHT
            if from_bottom <= settings.SHOPPING_LIST_MAX_Y:
                from_bottom = settings.SHOPPING_LIST_TITLE_Y
                pdf_file.showPage()
                pdf_file.setFont(font, settings.SHOPPING_LIST_SETFONT)
        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename="shopping_list.pdf"
        )


def add_favorite_shoppinglist(request, pk, model, serializer):
    recipe = get_object_or_404(Recipe, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        return Response(
            {"errors": "Рецепт уже есть в избранном или в списке покупок"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    model.objects.get_or_create(user=request.user, recipe=recipe)
    data = serializer(recipe).data
    return Response(data, status=status.HTTP_201_CREATED)


def remove_favorite_shoppinglist(request, pk, model):
    recipe = get_object_or_404(Recipe, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        follow = get_object_or_404(model, user=request.user,
                                   recipe=recipe)
        follow.delete()
        return Response(
            "Рецепт удален",
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        {"errors": "Рецепта несуществует"},
        status=status.HTTP_400_BAD_REQUEST
    )


def recipe_ingredient_create(ingredients_data, models, recipe):
    bulk_create_data = (
        models(
            recipe=recipe,
            ingredient=ingredient_data["ingredient"],
            amount=ingredient_data["amount"])
        for ingredient_data in ingredients_data
    )
    models.objects.bulk_create(bulk_create_data)
