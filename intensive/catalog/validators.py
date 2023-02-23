import django.core.exceptions
from django.utils.deconstruct import deconstructible


def excellent_validator(value):
    value = value.lower()
    if "превосходно" not in value and "роскошно" not in value:
        raise django.core.exceptions.ValidationError(
            "В значении должно "
            "обязательно содержаться слово `превосходно` или `роскошно`"
        )


@deconstructible
class ValidateMustContain:
    def __init__(self, *values):
        self.values = values
        self.message = (
            "В значении должно обязательно содержаться одно слово из"
            f" {self.values}"
        )

    def __call__(self, value):
        value = value.lower()
        if not any(v in value for v in self.values):
            raise django.core.exceptions.ValidationError(self.message)
