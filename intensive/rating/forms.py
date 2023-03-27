import django.forms

from .models import ItemRating


class ItemRatingForm(django.forms.ModelForm):
    class Meta:
        model = ItemRating
        fields = (
            ItemRating.score.field.name,
        )
        labels = {
            ItemRating.score.field.name: "Оценка"
        }
        help_text = {
            ItemRating.score.field.name: "Поставить оценку"
        }
        widgets = {
            ItemRating.score.field.name: django.forms.Select(attrs={"class": "form-control"})
        }
