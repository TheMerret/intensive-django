import django.core.exceptions


def excellent_validator(value):
    value = value.lower()
    if "превосходно" not in value and "роскошно" not in value:
        raise django.core.exceptions.ValidationError(
            "В значении должно "
            "обязательно содержаться слово `превосходно` или `роскошно`"
        )
