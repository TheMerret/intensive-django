from django import forms

import catalog.models


class ItemForm(forms.ModelForm):
    class Meta:
        model = catalog.models.Item
        fields = (catalog.models.Item.name.field.name,)
        labels = {
            catalog.models.Item.name.field.name: "Имя поля",
        }
        help_texts = {catalog.models.Item.name.field.name: "Подсказка"}
