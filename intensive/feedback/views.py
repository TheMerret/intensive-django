import django.conf
import django.contrib
import django.core.mail
import django.shortcuts
import django.urls
import django.views.generic

import feedback.forms
import feedback.models


class FeedbackView(django.views.generic.FormView):
    template_name = "feedback/feedback.html"
    form_class = feedback.forms.FeedbackForm
    success_url = django.urls.reverse_lazy("feedback:feedback")

    def form_valid(self, form):
        text = form.cleaned_data["text"]
        email = form.cleaned_data["email"]
        django.core.mail.send_mail(
            "Обратная связь.",
            f"Вы нам написали:\n\n{text}\n\nОбещаем все исправить!",
            django.conf.settings.FEEDBACK_EMAIL,
            [email],
            fail_silently=False,
        )
        contact = feedback.models.Contact(email=email)
        contact.save()
        fb = form.save(commit=False)
        fb.contact = contact
        fb.save()
        files = self.request.FILES.getlist("attachments")
        for file in files:
            attachment = feedback.models.Attachment(feedback=fb, file=file)
            attachment.save()
        django.contrib.messages.success(self.request, "Сообщение отправлено")
        return super().form_valid(form)
