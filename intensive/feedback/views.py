import django.conf
import django.contrib
import django.core.mail
import django.shortcuts

import feedback.forms
import feedback.models


def feedback_view(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(
        request.POST or None, request.FILES or None
    )
    context = {"form": form}
    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data["text"]
        email = form.cleaned_data["email"]
        django.core.mail.send_mail(
            "Обратная связь.",
            f"Вы нам написали:\n\n{text}\n\nОбещаем все исправить!",
            django.conf.settings.FEEDBACK_EMAIL,
            [email],
            fail_silently=False,
        )
        fb = form.save()
        files = request.FILES.getlist("attachments")
        for file in files:
            attachment = feedback.models.Attachment(feedback=fb, file=file)
            attachment.save()
        django.contrib.messages.success(request, "Сообщение отправлено")
        return django.shortcuts.redirect("feedback:feedback")
    return django.shortcuts.render(request, template, context)
