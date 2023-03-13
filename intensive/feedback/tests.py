import django.test
import django.urls

import feedback.forms
import feedback.models


class FeedbackTests(django.test.TransactionTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_form_key_in_context(self):
        """test that key form is in context"""
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback")
        )
        self.assertIn("form", response.context)

    def test_form_in_context_is_feedbackform(self):
        """test that form in context is instance of FeedbackForm"""
        response = django.test.Client().get(
            django.urls.reverse("feedback:feedback")
        )
        form = response.context["form"]
        self.assertIsInstance(form, feedback.forms.FeedbackForm)

    def test_text_label_correct(self):
        """test text field label is correct"""
        text_label = self.form.fields["text"].label
        self.assertEqual(text_label, "Текст обратной связи")

    def test_text_help_text(self):
        """test text field help text is correct"""
        text_help_text = self.form.fields["text"].help_text
        self.assertEqual(text_help_text, "Что вы хотите сообщить нам")

    def test_mail_label_correct(self):
        """test mail field label is correct"""
        mail_label = self.form.fields["email"].label
        self.assertEqual(mail_label, "Почта")

    def test_mail_help_text(self):
        """test mail field help text is correct"""
        mail_help_text = self.form.fields["email"].help_text
        self.assertEqual(mail_help_text, "Ваша почта")

    def test_redirect(self):
        """test after form input redirects back"""
        data = {"text": "Test text", "email": "test@test.ru"}
        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"), data=data, follow=True
        )
        self.assertRedirects(
            response, django.urls.reverse("feedback:feedback")
        )

    def test_feedback_record_saved(self):
        """test after form input new feedback record saved"""
        feedbacks_count = feedback.models.Feedback.objects.count()
        data = {"text": "Test text", "email": "test@test.ru"}
        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"), data=data
        )
        self.assertRedirects(
            response, django.urls.reverse("feedback:feedback")
        )
        self.assertEqual(
            feedbacks_count + 1, feedback.models.Feedback.objects.count()
        )

    def test_feedback_attachments_saved(self):
        """test after form input with attachments new attachments
          records saved"""
        attachments_count = feedback.models.Attachment.objects.count()
        with open("feedback/fixtures/file.jpg", "rb") as f1, open(
            "feedback/fixtures/file.txt", "r"
        ) as f2:
            data = {
                "text": "Test text",
                "email": "test@test.ru",
                "attachments": [f1, f2],
            }
            django.test.Client().post(
                django.urls.reverse("feedback:feedback"), data=data
            )

        self.assertEqual(
            attachments_count + 2,  # two files sent
            feedback.models.Attachment.objects.count(),
        )
        # however directories stay
        feedback.models.Attachment.objects.all().delete()
