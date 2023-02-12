import re


REQUEST_COUT = 10


class ReverseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0

    def __call__(self, request):
        self.request_count += 1
        response = self.get_response(request)
        text = response.content.decode("utf-8")

        if self.request_count % REQUEST_COUT == 0:
            russian_words_pattern = re.compile(r"\b[а-я]+", re.IGNORECASE)
            text_with_reversed = russian_words_pattern.sub(
                lambda m: m.group()[::-1], text
            )
            response.content = text_with_reversed.encode()
            self.request_count = 0
        return response
