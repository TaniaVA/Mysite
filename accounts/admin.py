from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CustomerPhoto


class PhotosInline(admin.TabularInline):
    model = CustomerPhoto
    extra = 1

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_staff",
    ]
    inlines = [
        PhotosInline,
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ()}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ()}),)

admin.site.register(CustomUser, CustomUserAdmin)