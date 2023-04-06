from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CustomerPhoto


# This is an inline class for the CustomerPhoto model
# which allows the user to add/edit photos associated
# with a user from the user admin page.
# TabularInline is a subclass of admin.
# StackedInline which displays the related objects in a tabular format.
class PhotosInline(admin.TabularInline):
    model = CustomerPhoto
# This specifies the number of extra forms that will be displayed in the inline formset.
    extra = 1


# This is the main admin class for the CustomUser model which inherits from the built-in UserAdmin class.
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
