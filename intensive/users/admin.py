from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile


class InlineProfile(admin.TabularInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (InlineProfile, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
