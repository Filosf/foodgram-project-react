import io

from django.db.models import Sum
from django.conf import settings
from django.http import FileResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.views import APIView

from recipes.models import RecipeIngredients


class ShoppingListDownloadView(APIView):
    def get(self, request):
        user = request.user
        shopping_list = RecipeIngredients.objects.filter(
            recipe__cart__user=user).values(
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
