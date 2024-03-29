# Generated by Django 3.2.17 on 2023-02-27 19:11

import catalog.validators
from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=tinymce.models.HTMLField(help_text='Введите описание объекта', validators=[catalog.validators.ValidateMustContain('превосходно', 'роскошно')], verbose_name='Описание'),
        ),
    ]
