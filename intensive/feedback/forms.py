import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    attachments = django.forms.FileField(
        label=feedback.models.Attachment.file.field.verbose_name.capitalize(),
        widget=django.forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
        help_text=feedback.models.Attachment.file.field.help_text,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.text.field.name,
            feedback.models.Feedback.email.field.name,
        )
