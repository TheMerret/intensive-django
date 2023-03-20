# Generated by Django 3.2.17 on 2023-03-19 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields
import users.models


def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('users', 'Profile')

    for user in User.objects.all():
        Profile.objects.create(user=user)


def remove_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    for user in User.objects.all():
        user.profile.delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='дата рождения')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=users.models.get_user_media_path, verbose_name='фото')),
                ('coffee_count', models.PositiveIntegerField(default=0, verbose_name='количество выпитых кофе')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Дополнительное поле',
                'verbose_name_plural': 'Дополнительные поля',
            },
        ),
        migrations.RunPython(create_profiles, reverse_code=remove_profiles)
    ]