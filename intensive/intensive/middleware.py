import re

from django.conf import settings


class ReverseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.russian_words_pattern = re.compile(r"\b[а-я]+", re.IGNORECASE)

    def __call__(self, request):
        self.request_count += 1
        response = self.get_response(request)

        if not settings.REVERSE_REQUEST_COUNT:
            return response

        if self.request_count % settings.REVERSE_REQUEST_COUNT == 0:
            text = response.content.decode("utf-8")
            text_with_reversed = self.russian_words_pattern.sub(
                lambda m: m.group()[::-1], text
            )
            response.content = text_with_reversed.encode()
            self.request_count = 0
        return response
