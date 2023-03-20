# Generated by Django 3.2.17 on 2023-03-13 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_attachments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Ваша почта', max_length=150, verbose_name='почта')),
            ],
            options={
                'verbose_name': 'контакты',
                'verbose_name_plural': 'контакты',
            },
        ),
        migrations.AddField(
            model_name='feedback',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='feedback.contact', verbose_name='контакты'),
        ),
    ]