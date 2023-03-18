from django import forms


def starts_with_a(value):
    if not value.startswith("А"):
        raise forms.ValidationError("Дожно начинаться с А")


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Имечко",
        max_length=100,
        validators=[starts_with_a],
    )
    email = forms.EmailField(
        label="Почтенка",
        max_length=100,
    )
