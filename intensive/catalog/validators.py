import re

import django.core.exceptions
from django.utils.deconstruct import deconstructible
from django.utils.html import strip_tags


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
        word_groups = "|".join(values)
        self.words_regex = re.compile(
            rf"\b({word_groups})\b", flags=re.IGNORECASE
        )
        self.values = values
        self.message = (
            "В значении должно обязательно содержаться одно слово из"
            f" {self.values}"
        )

    def __call__(self, value):
        value = strip_tags(value)
        if not self.words_regex.search(value):
            raise django.core.exceptions.ValidationError(self.message)
