import django.utils.timezone

import users.models


def birthdays(request):
    tzname = request.COOKIES.get("django_timezone")
    with django.utils.timezone.override(tzname):
        birtday_users = users.models.UserProxy.objects.birthdays()
    return {"birthdays": birtday_users}
